from okex_api import *
import funding_rate
import open_position
import close_position
import trading_data
from datetime import datetime, timedelta
import record
import threading
from log import fprint


# 监控一个币种，如果当期资金费+预测资金费小于重新开仓成本（开仓期现差价-平仓期现差价-手续费），进行平仓。
# 如果合约仓位到达下级杠杆，进行减仓。如果合约仓位到达上级杠杆，进行加仓。
# 如果距离下期资金费3小时以上，（开仓期现差价-平仓期现差价-手续费）>0.2%，进行套利。
class Monitor(OKExAPI):
    """监控功能类
    """

    def __init__(self, coin, accountid):
        OKExAPI.__init__(self, coin, accountid)

    def liquidation_price(self):
        """获取强平价
        """
        holding = self.swap_holding()
        if holding:
            return float(holding['liquidation_price'])
        else:
            return 0.

    def apr(self, days=0):
        """最近年利率

        :param days: 最近几天，默认开仓算起
        :rtype: float
        """
        Stat = trading_data.Stat(self.coin)
        swap_margin = self.swap_margin()
        spot_position = self.spot_position()
        last = float(self.spotAPI.get_specific_ticker(self.spot_ID)['last'])
        holding = swap_margin + last * spot_position
        timestamp = datetime.utcnow()

        if holding > 10:
            if days == 0:
                open_time = Stat.open_time(self.accountid)
                delta = timestamp.__sub__(open_time).total_seconds()
                funding = Stat.history_funding(self.accountid)
                cost = Stat.history_cost(self.accountid)
                apr = (funding + cost) / holding / delta * 86400 * 365
            else:
                funding = Stat.history_funding(self.accountid, days)
                cost = Stat.history_cost(self.accountid, days)
                apr = (funding + cost) / holding / days * 365
        else:
            apr = 0.
        return apr

    def apy(self, days=0):
        """最近年化

        :param days: 最近几天，默认开仓算起
        :rtype: float
        """
        import math
        return math.exp(self.apr(days)) - 1

    def back_tracking(self):
        """补录最近七天资金费
        """
        Ledger = record.Record('Ledger')
        ledger = self.swapAPI.get_ledger(instrument_id=self.swap_ID, limit='100', type='14')
        count = 0
        for item in ledger[0]:
            realized_rate = float(item['amount'])
            timestamp: str = item['timestamp']
            timestamp: datetime = record.fromiso8601(timestamp)
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "资金费",
                      'funding': realized_rate}
            # 查重
            if not Ledger.mycol.find_one(mydict):
                Ledger.mycol.insert_one(mydict)
                count += 1
        fprint(back_track_funding.format(self.coin, count))

    def record_funding(self):
        Ledger = record.Record('Ledger')
        ledger = self.swapAPI.get_ledger(instrument_id=self.swap_ID, limit='1', type='14')
        realized_rate = float(ledger[0][0]['amount'])
        timestamp = record.fromiso8601(ledger[0][0]['timestamp'])
        fprint(received_funding.format(self.coin, realized_rate))
        mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "资金费",
                  'funding': realized_rate}
        Ledger.mycol.insert_one(mydict)
        fprint(received_funding.format(self.coin, realized_rate))

    def position_exist(self):
        """判断是否有仓位
        """
        if self.swap_position() == 0:
            # print(self.coin, "没有仓位")
            return False
        else:
            result = record.Record('Ledger').find_last({'account': self.accountid, 'instrument': self.coin})
            if result and result['title'] == '平仓':
                # print(self.coin, "已平仓")
                return False
        return True

    def rebalance(self, leverage=0):
        """仓位杠杆再平衡

        :param leverage: 杠杆
        """
        timestamp = datetime.utcnow()
        addPosition = open_position.AddPosition(self.coin, self.accountid)
        reducePosition = close_position.ReducePosition(self.coin, self.accountid)
        Stat = trading_data.Stat(self.coin)
        Ledger = record.Record('Ledger')
        current_lever = self.get_lever()

        if leverage:
            if leverage > current_lever:
                addPosition.set_lever(leverage)
            elif leverage < current_lever:
                pass
            else:
                pass
        else:
            leverage = current_lever
        liquidation_price = self.liquidation_price()
        swap_ticker = self.swapAPI.get_specific_ticker(self.swap_ID)
        last = float(swap_ticker['last'])
        # 实际杠杆大于目标
        if liquidation_price < last * (1 + 1 / leverage):
            fprint("再平衡减仓")
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "手动再平衡"}
            Ledger.mycol.insert_one(mydict)
            swap_position = self.swap_position()
            target_size = swap_position * (1 - liquidation_price / last / (1 + 1 / leverage))

            # 期现差价控制在2个标准差
            recent = Stat.recent_close_stat()
            close_pd = recent['avg'] - 2 * recent['std']

            reducePosition.reduce(target_size=target_size, price_diff=close_pd, accelerate_after=2)
            addPosition.set_lever(leverage)

        # 实际杠杆小于目标
        if liquidation_price > last * (1 + 1 / leverage):
            fprint("再平衡加仓")
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "手动再平衡"}
            Ledger.mycol.insert_one(mydict)
            swap_position = self.swap_position()
            target_size = swap_position * (liquidation_price / last / (1 + 1 / leverage) - 1)
            transfer_amount = target_size * last

            # 期现差价控制在2个标准差
            recent = Stat.recent_open_stat()
            open_pd = recent['avg'] + 2 * recent['std']

            if self.transfer_to_spot(transfer_amount=transfer_amount):
                addPosition.add(target_size=target_size, leverage=leverage, price_diff=open_pd, accelerate_after=2)

    def watch(self):
        """监控仓位，自动加仓、减仓
        """
        if not self.position_exist():
            exit()
        fprint(start_monitoring, self.coin)

        fundingRate = funding_rate.FundingRate()
        addPosition = open_position.AddPosition(self.coin, self.accountid)
        reducePosition = close_position.ReducePosition(self.coin, self.accountid)
        Stat = trading_data.Stat(self.coin)
        Ledger = record.Record('Ledger')
        OP = record.Record('OP')

        # 计算手续费
        spot_trade_fee = float(self.spotAPI.get_trade_fee(instrument_id=self.spot_ID)['taker'])
        swap_trade_fee = float(self.swapAPI.get_trade_fee(instrument_id=self.swap_ID)['taker'])
        trade_fee = swap_trade_fee + spot_trade_fee
        leverage = self.get_lever()

        liquidation_price = self.liquidation_price()
        thread_started = False
        time_to_accelerate = None
        accelerated = False
        add = threading.Thread()
        reduce = threading.Thread()
        retry = 0

        while True:
            timestamp = datetime.utcnow()
            begin = timestamp
            swap_ticker = self.swapAPI.get_specific_ticker(self.swap_ID)
            last = float(swap_ticker['last'])

            # 每小时更新一次资金费，强平价
            if timestamp.minute == 1:
                if timestamp.second < 10:
                    current_rate = fundingRate.current(self.swap_ID)
                    next_rate = fundingRate.next(self.swap_ID)
                    liquidation_price = self.liquidation_price()

                    if liquidation_price == 0:
                        exit()

                    recent = Stat.recent_open_stat()
                    open_pd = recent['avg'] + recent['std']
                    recent = Stat.recent_close_stat()
                    close_pd = recent['avg'] - recent['std']

                    cost = open_pd - close_pd - 2 * trade_fee
                    if (timestamp.hour + 4) % 8 == 0 and current_rate + next_rate < cost:
                        fprint(coin_current_next)
                        fprint('{:6s}{:9.3%}{:11.3%}'.format(self.coin, current_rate, next_rate))
                        fprint(cost_to_close.format(cost))
                        fprint(proceed_to_close, self.coin)
                        reducePosition.close(price_diff=close_pd)
                        break

                    if timestamp.hour % 8 == 0:
                        self.record_funding()
                        fprint(coin_current_next)
                        fprint('{:6s}{:9.3%}{:11.3%}'.format(self.coin, current_rate, next_rate))

            # 线程未创建
            if not thread_started:
                # 接近强平价，现货减仓
                if liquidation_price < last * (1 + 1 / (leverage + 1)):
                    if OP.find_last({'account': self.accountid, 'instrument': self.coin}):
                        timestamp = datetime.utcnow()
                        delta = timestamp.__sub__(begin).total_seconds()
                        if delta < 10:
                            time.sleep(10 - delta)
                        continue
                    if not addPosition.is_hedged():
                        fprint(self.coin, hedge_fail)
                        exit()
                    fprint(approaching_liquidation)
                    mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp,
                              'title': "自动减仓"}
                    Ledger.mycol.insert_one(mydict)
                    swap_position = self.swap_position()
                    target_size = swap_position / (leverage + 1) ** 2

                    # 期现差价控制在1.5个标准差
                    recent = Stat.recent_close_stat()
                    close_pd = recent['avg'] - 1.5 * recent['std']

                    reduce = threading.Thread(target=reducePosition.reduce,
                                              kwargs={'target_size': target_size, 'price_diff': close_pd})
                    reduce.start()
                    thread_started = True
                    time_to_accelerate = datetime.utcnow() + timedelta(hours=2)

                # 保证金过多，现货加仓
                if liquidation_price > last * (1 + 1 / (leverage - 1)):
                    if OP.find_last({'account': self.accountid, 'instrument': self.coin}):
                        timestamp = datetime.utcnow()
                        delta = timestamp.__sub__(begin).total_seconds()
                        if delta < 10:
                            time.sleep(10 - delta)
                        continue
                    if not addPosition.is_hedged():
                        fprint(self.coin, hedge_fail)
                        exit()
                    fprint(too_much_margin)
                    mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp,
                              'title': "自动加仓"}
                    Ledger.mycol.insert_one(mydict)
                    swap_position = self.swap_position()
                    target_size = swap_position * (liquidation_price / last / (1 + 1 / leverage) - 1)

                    # 期现差价控制在2个标准差
                    recent = Stat.recent_open_stat()
                    open_pd = recent['avg'] + 2 * recent['std']

                    swap_balance = self.swap_balance()
                    transfer_amount = min(target_size * last, swap_balance)
                    # print("target_size {}, swap_balance {}, transfer_amount {}".format(target_size, swap_balance, transfer_amount))
                    if self.transfer_to_spot(transfer_amount=transfer_amount):
                        add = threading.Thread(target=addPosition.add,
                                               kwargs={'target_size': target_size, 'leverage': leverage,
                                                       'price_diff': open_pd})
                        add.start()
                        thread_started = True
                        time_to_accelerate = datetime.utcnow() + timedelta(hours=2)
                    else:
                        retry += 1
                        if retry == 3:
                            print(reach_max_retry)
                            exit()
            # 线程已运行
            else:
                # 如果减仓时间过长，加速减仓
                if reduce.is_alive():
                    # 迫近下下级杠杆
                    if liquidation_price < last * (1 + 1 / (leverage + 2)) and not accelerated:
                        # 已加速就不另开线程
                        reducePosition.exitFlag = True
                        while reduce.is_alive():
                            time.sleep(1)

                        liquidation_price = self.liquidation_price()
                        swap_position = self.swap_position()
                        target_size = swap_position * (1 - liquidation_price / last / (1 + 1 / leverage))
                        recent = Stat.recent_close_stat(1)
                        close_pd = recent['avg'] - 1.5 * recent['std']
                        reduce = threading.Thread(target=reducePosition.reduce,
                                                  kwargs={'target_size': target_size, 'price_diff': close_pd})
                        reducePosition.exitFlag = False
                        accelerated = True
                        reduce.start()
                        time_to_accelerate = datetime.utcnow() + timedelta(hours=2)

                    if timestamp > time_to_accelerate:
                        reducePosition.exitFlag = True
                        while reduce.is_alive():
                            time.sleep(1)

                        liquidation_price = self.liquidation_price()
                        swap_position = self.swap_position()
                        target_size = swap_position * (1 - liquidation_price / last / (1 + 1 / leverage))
                        recent = Stat.recent_close_stat(2)
                        close_pd = recent['avg'] - 1.5 * recent['std']
                        reduce = threading.Thread(target=reducePosition.reduce,
                                                  kwargs={'target_size': target_size, 'price_diff': close_pd})
                        reducePosition.exitFlag = False
                        reduce.start()
                        time_to_accelerate = datetime.utcnow() + timedelta(hours=2)
                elif add.is_alive():
                    if timestamp > time_to_accelerate:
                        addPosition.exitFlag = True
                        while add.is_alive():
                            time.sleep(1)

                        liquidation_price = self.liquidation_price()
                        swap_position = self.swap_position()
                        target_size = swap_position * (liquidation_price / last / (1 + 1 / leverage) - 1)
                        recent = Stat.recent_open_stat(2)
                        open_pd = recent['avg'] + 2 * recent['std']
                        add = threading.Thread(target=addPosition.add,
                                               kwargs={'target_size': target_size, 'leverage': leverage,
                                                       'price_diff': open_pd})
                        addPosition.exitFlag = False
                        add.start()
                        time_to_accelerate = datetime.utcnow() + timedelta(hours=2)
                else:
                    liquidation_price = self.liquidation_price()
                    thread_started = False
            timestamp = datetime.utcnow()
            delta = timestamp.__sub__(begin).total_seconds()
            if delta < 10:
                time.sleep(10 - delta)
