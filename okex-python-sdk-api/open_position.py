from okex_api import *
from datetime import datetime, timedelta
import record
import trading_data
from log import fprint


class AddPosition(OKExAPI):
    """建仓、加仓功能类
    """

    def __init__(self, coin, accountid):
        OKExAPI.__init__(self, coin, accountid)

    def is_hedged(self):
        """判断合约现货是否对冲
        """
        contract_val = float(self.swap_info['contract_val'])
        short = self.swap_position()
        long = self.spot_position()

        if abs(long - short) < contract_val:
            return True
        else:
            fprint(self.coin, spot_text, long, swap_text, short)
            return False

    def hedge(self):
        """加仓以达到完全对冲
        """

    def transfer(self, usdt_size=0.0, leverage=2):
        """根据仓位和杠杆划转资金

        :param usdt_size: 目标仓位
        :param leverage: 杠杆
        :return: 是否成功
        """
        last = float(self.spotAPI.get_specific_ticker(self.spot_ID)['last'])
        target_position = usdt_size * leverage / (leverage + 1) / last

        usdt_balance = self.usdt_balance()
        swap_balance = self.swap_balance()

        if usdt_size > usdt_balance + swap_balance:
            fprint(insufficient_USDT)
            return False
        elif usdt_balance >= target_position * last:
            if swap_balance >= target_position * last / leverage:
                return True
            else:
                fprint(insufficient_margin)
                transfer_amount = target_position * last / leverage - swap_balance
                # 资金划转
                # result = self.accountAPI.coin_transfer(currency='', amount='', account_from='', account_to='',
                #                                        type='',sub_account='', instrument_id='', to_instrument_id='')
                try:
                    transfer = self.accountAPI.coin_transfer(currency='USDT', amount=str(transfer_amount),
                                                             account_from='1', account_to='9', instrument_id='',
                                                             to_instrument_id=self.spot_ID)
                    if transfer['result']:
                        fprint(transfer_text + str(transfer_amount) + "USDT" + to_swap_account)
                        return True
                    else:
                        return False
                except OkexAPIException as e:
                    fprint(e)
                    fprint(transfer_failed)
                    return False
        else:
            fprint(insufficient_USDT)
            transfer_amount = target_position * last - usdt_balance
            # 资金划转
            # result = self.accountAPI.coin_transfer(currency='', amount='', account_from='', account_to='', type='',
            #                                        sub_account='', instrument_id='', to_instrument_id='')
            try:
                transfer = self.accountAPI.coin_transfer(currency='USDT', amount=str(transfer_amount),
                                                         account_from='9', account_to='1', instrument_id=self.spot_ID,
                                                         to_instrument_id='')
                if transfer['result']:
                    fprint(transfer_text + str(transfer_amount) + "USDT" + to_spot_account)
                    return True
                else:
                    return False
            except OkexAPIException as e:
                fprint(e)
                fprint(transfer_failed)
                return False

    def set_lever(self, leverage: int):
        # 获取某个合约的用户配置
        setting = self.swapAPI.get_settings(self.swap_ID)
        while setting['margin_mode'] != 'crossed' or int(float(setting['short_leverage'])) != leverage:
            # 设定某个合约的杠杆
            fprint(current_leverage, setting['short_leverage'])
            fprint(set_leverage, leverage)
            self.swapAPI.set_leverage(instrument_id=self.swap_ID, leverage='{:d}'.format(leverage), side='3')
            time.sleep(1)
            setting = self.swapAPI.get_settings(self.swap_ID)
            # print(setting)

    def add(self, usdt_size=0.0, target_size=0.0, leverage=2, price_diff=0.002, accelerate_after=0):
        """加仓期现组合

        :param usdt_size: U本位目标仓位
        :param target_size: 币本位目标仓位
        :param leverage: 杠杆
        :param price_diff: 期现差价
        :param accelerate_after: 几小时后加速
        :return: 加仓数量
        :rtype: float
        """
        if usdt_size:
            last = float(self.spotAPI.get_specific_ticker(self.spot_ID)['last'])
            target_position = usdt_size * leverage / (leverage + 1) / last
        else:
            target_position = target_size
        fprint(self.coin, amount_to_add, target_position)
        OP = record.Record('OP')
        mydict = {'account': self.accountid, 'instrument': self.coin, 'op': 'add'}
        OP.mycol.insert_one(mydict)

        min_size = float(self.spot_info['min_size'])
        size_increment = float(self.spot_info['size_increment'])
        contract_val = float(self.swap_info['contract_val'])

        # 现货手续费率
        trade_fee = float(self.spotAPI.get_trade_fee(instrument_id=self.spot_ID)['taker'])

        self.set_lever(leverage)

        counter = 0
        filled_sum = 0
        fee_total = 0
        spot_notional = 0
        swap_notional = 0
        time_to_accelerate = datetime.utcnow() + timedelta(hours=accelerate_after)
        Stat = trading_data.Stat(self.coin)
        # 如果仍未建仓完毕
        while target_position >= contract_val and not self.exitFlag:
            # 判断是否加速
            if accelerate_after and datetime.utcnow() > time_to_accelerate:
                recent = Stat.recent_open_stat(accelerate_after)
                price_diff = recent['avg'] + 2 * recent['std']
                time_to_accelerate = datetime.utcnow() + timedelta(hours=accelerate_after)

            # 公共-获取现货ticker信息
            # spot_ticker = self.spotAPI.get_specific_ticker(self.spot_ID)
            # 公共-获取合约ticker信息
            # swap_ticker = self.swapAPI.get_specific_ticker(self.swap_ID)
            tickers = self.parallel_ticker()
            spot_ticker = tickers[0]
            swap_ticker = tickers[1]
            # 现货最低买入价
            best_ask = float(spot_ticker['best_ask'])
            # 合约最高卖出价
            best_bid = float(swap_ticker['best_bid'])

            # 如果不满足期现溢价
            if best_bid < best_ask * (1 + price_diff):
                # print("当前期现差价: ", (best_bid - best_ask) / best_ask, "<", price_diff)
                counter = 0
                time.sleep(SLEEP)
            # 监视溢价持久度
            else:
                if counter < CONFIRMATION:
                    counter += 1
                    time.sleep(SLEEP)
                else:
                    # 查询账户余额
                    usdt_balance = self.usdt_balance()
                    swap_balance = self.swap_balance()

                    # 更新价格
                    tickers = self.parallel_ticker()
                    spot_ticker = tickers[0]
                    swap_ticker = tickers[1]
                    best_ask = float(spot_ticker['best_ask'])
                    last = float(spot_ticker['last'])
                    best_bid = float(swap_ticker['best_bid'])

                    if usdt_balance < target_position * last:
                        while usdt_balance < target_position * last:
                            target_position -= min_size
                        if target_position < min_size:
                            fprint(insufficient_USDT)
                            break
                    elif swap_balance < target_position * last / leverage:
                        while swap_balance < target_position * last / leverage:
                            target_position -= contract_val
                        if target_position < contract_val:
                            fprint(insufficient_margin)
                            break
                    else:
                        # 计算下单数量
                        best_ask_size = float(spot_ticker['best_ask_size'])
                        best_bid_size = float(swap_ticker['best_bid_size'])
                        # print(best_ask_size, best_bid_size)
                        # continue
                        order_size = min(target_position, round_to(best_ask_size, min_size),
                                         best_bid_size * contract_val)
                        order_size = round_to(order_size, contract_val)

                        # 考虑现货手续费，分别计算现货数量与合约张数
                        contract_size = round(order_size / contract_val)
                        spot_size = round_to(order_size / (1 - trade_fee), size_increment)
                        # print(order_size, contract_size, spot_size)

                        # 下单
                        if order_size > 0:
                            try:
                                # 现货下单（Fill or Kill）
                                kwargs = {'instrument_id': self.spot_ID, 'side': 'buy', 'size': str(spot_size),
                                          'price': best_ask, 'order_type': '2'}
                                thread1 = MyThread(target=self.spotAPI.take_order, kwargs=kwargs)
                                thread1.start()

                                # 合约下单（Fill or Kill）
                                kwargs = {'instrument_id': self.swap_ID, 'type': '2', 'size': str(contract_size),
                                          'price': best_bid, 'order_type': '2'}
                                thread2 = MyThread(target=self.swapAPI.take_order, kwargs=kwargs)
                                thread2.start()

                                thread1.join()
                                thread2.join()
                                spot_order = thread1.get_result()
                                swap_order = thread2.get_result()
                            except OkexAPIException as e:
                                if e.message == "System error" or e.code == "35003":
                                    fprint(futures_market_down)
                                    spot_order = thread1.get_result()
                                    spot_order_info = self.spotAPI.get_order_info(instrument_id=self.spot_ID,
                                                                                  order_id=spot_order['order_id'])
                                    fprint(spot_order_info)
                                fprint(e)
                                break

                            if spot_order['order_id'] != '-1' and swap_order['order_id'] != '-1':
                                spot_order_info = self.spotAPI.get_order_info(instrument_id=self.spot_ID,
                                                                              order_id=spot_order['order_id'])
                                swap_order_info = self.swapAPI.get_order_info(instrument_id=self.swap_ID,
                                                                              order_id=swap_order['order_id'])
                                spot_order_state = spot_order_info['state']
                                swap_order_state = swap_order_info['state']
                            else:
                                if spot_order['order_id'] == '-1':
                                    fprint(spot_order_failed)
                                    fprint(spot_order)
                                else:
                                    fprint(swap_order_failed)
                                    fprint(swap_order)
                                break

                            while spot_order_state != '2' or swap_order_state != '2':
                                # print(spot_order_state+','+swap_order_state)
                                if spot_order_state == '2':
                                    if swap_order_state in ['-1', '-2']:
                                        fprint(swap_order_retract, swap_order_state)
                                        try:
                                            # 市价开空合约
                                            swap_order = self.swapAPI.take_order(instrument_id=self.swap_ID, type='2',
                                                                                 size=str(contract_size),
                                                                                 order_type='4', price='')
                                        except Exception as e:
                                            fprint(e)
                                            return 0
                                    else:
                                        fprint(swap_order_state, swap_order_state)
                                        fprint(await_status_update)
                                elif swap_order_state == '2':
                                    if spot_order_state in ['-1', '-2']:
                                        fprint(spot_order_retract, spot_order_state)
                                        # 重新定价
                                        tick_size = float(self.spot_info['tick_size'])
                                        limit_price = best_ask * (1 + 0.02)
                                        limit_price = str(round_to(limit_price, tick_size))
                                        try:
                                            spot_order = self.spotAPI.take_order(instrument_id=self.spot_ID, side='buy',
                                                                                 size=str(spot_size), price=limit_price,
                                                                                 type='limit')
                                        except Exception as e:
                                            fprint(e)
                                            return 0
                                    else:
                                        fprint(spot_order_state, spot_order_state)
                                        fprint(await_status_update)
                                elif spot_order_state in ['-1', '-2'] and swap_order_state in ['-1', '-2']:
                                    # print("下单失败")
                                    break
                                else:
                                    fprint(await_status_update)

                                if spot_order['order_id'] != '-1' and swap_order['order_id'] != '-1':
                                    spot_order_info = self.spotAPI.get_order_info(instrument_id=self.spot_ID,
                                                                                  order_id=spot_order['order_id'])
                                    swap_order_info = self.swapAPI.get_order_info(instrument_id=self.swap_ID,
                                                                                  order_id=swap_order['order_id'])
                                    spot_order_state = spot_order_info['state']
                                    swap_order_state = swap_order_info['state']
                                    time.sleep(SLEEP)
                                else:
                                    if spot_order['order_id'] == '-1':
                                        fprint(spot_order_failed)
                                        fprint(spot_order)
                                    else:
                                        fprint(swap_order_failed)
                                        fprint(swap_order)
                                    fprint(added_amount, filled_sum, self.coin)
                                    return filled_sum

                            if spot_order_state == '2' and swap_order_state == '2':
                                spot_filled = float(spot_order_info['filled_size'])
                                swap_filled = float(swap_order_info['filled_qty']) * contract_val
                                filled_sum += swap_filled
                                spot_price = float(spot_order_info['price_avg'])
                                fee_total += float(spot_order_info['fee']) * spot_price
                                spot_notional -= float(spot_order_info['filled_notional'])
                                fee_total += float(swap_order_info['fee'])
                                swap_price = float(swap_order_info['price_avg'])
                                swap_notional += swap_filled * swap_price
                                if abs(spot_filled - swap_filled) < contract_val:
                                    target_position -= swap_filled
                                    fprint(hedge_success, swap_filled, remaining + str(target_position))
                                else:
                                    fprint(hedge_fail)
                                    break

                            usdt_balance = self.usdt_balance()
                            swap_balance = self.swap_balance()
                            target_position = min(target_position, usdt_balance / best_ask,
                                                  swap_balance / best_bid * leverage)
                            counter = 0
                        else:
                            # print("订单太小", order_size)
                            time.sleep(SLEEP)
        if spot_notional != 0:
            Ledger = record.Record('Ledger')
            timestamp = datetime.utcnow()
            mylist = []
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "现货买入",
                      'spot_notional': spot_notional}
            mylist.append(mydict)
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "合约开空",
                      'swap_notional': swap_notional}
            mylist.append(mydict)
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "手续费",
                      'fee': fee_total}
            mylist.append(mydict)
            Ledger.mycol.insert_many(mylist)

        mydict = {'account': self.accountid, 'instrument': self.coin, 'op': 'add'}
        OP.mycol.delete_one(mydict)
        fprint(added_amount, filled_sum, self.coin)
        return filled_sum

    def open(self, usdt_size=0.0, target_size=0.0, leverage=2, price_diff=0.002, accelerate_after=0):
        """建仓期现组合

        :param usdt_size: U本位目标仓位
        :param target_size: 币本位目标仓位
        :param leverage: 杠杆
        :param price_diff: 期现差价
        :param accelerate_after: 几小时后加速
        :return: 建仓数量
        :rtype: float
        """
        Ledger = record.Record('Ledger')
        result = Ledger.find_last({'account': self.accountid, 'instrument': self.coin})
        if result and result['title'] != '平仓':
            fprint(position_exist, self.swap_position(), self.coin)
        else:
            timestamp = datetime.utcnow()
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "开仓"}
            Ledger.mycol.insert_one(mydict)

        if target_size:
            last = float(self.spotAPI.get_specific_ticker(self.spot_ID)['last'])
            usdt_size = last * target_size * (1 + 1 / leverage)
        if self.transfer(usdt_size=usdt_size, leverage=leverage):
            return self.add(usdt_size=usdt_size, leverage=leverage, price_diff=price_diff,
                            accelerate_after=accelerate_after)
        else:
            fprint(insufficient_USDT)
