from okex_api import *
from datetime import datetime, timedelta
import record
import trading_data
from log import fprint


class ReducePosition(OKExAPI):
    """平仓、减仓功能类
    """

    def __init__(self, coin, accountid):
        OKExAPI.__init__(self, coin, accountid)

    def hedge(self):
        """减仓以达到完全对冲
        """

    def reduce(self, usdt_size=0.0, target_size=0.0, price_diff=0.002, accelerate_after=0):
        """减仓期现组合

        :param usdt_size: U本位目标仓位
        :param target_size: 币本位目标仓位
        :param price_diff: 期现差价
        :param accelerate_after: 几小时后加速
        :return: 卖现货所得USDT
        :rtype: float
        """
        if usdt_size:
            last = float(self.spotAPI.get_specific_ticker(self.spot_ID)['last'])
            leverage = self.get_lever()
            target_position = usdt_size * leverage / (leverage + 1) / last
        else:
            target_position = target_size

        min_size = float(self.spot_info['min_size'])
        size_increment = float(self.spot_info['size_increment'])
        contract_val = float(self.swap_info['contract_val'])

        spot_position = self.spot_position()
        swap_position = self.swap_position()

        if target_position > spot_position or target_position > swap_position:
            self.close(price_diff, accelerate_after)
        else:
            fprint(self.coin, amount_to_reduce, target_position)
            OP = record.Record('OP')
            mydict = {'account': self.accountid, 'instrument': self.coin, 'op': 'reduce'}
            OP.mycol.insert_one(mydict)

            counter = 0
            filled_sum = 0.
            usdt_release = 0.
            fee_total = 0.
            spot_notional = 0.
            swap_notional = 0.
            time_to_accelerate = datetime.utcnow() + timedelta(hours=accelerate_after)
            Stat = trading_data.Stat(self.coin)
            # 如果仍未减仓完毕
            while target_position >= contract_val and not self.exitFlag:
                # 判断是否加速
                if accelerate_after and datetime.utcnow() > time_to_accelerate:
                    recent = Stat.recent_close_stat(accelerate_after)
                    price_diff = recent['avg'] - 2 * recent['std']
                    time_to_accelerate = datetime.utcnow() + timedelta(hours=accelerate_after)

                # 公共-获取现货ticker信息
                # spot_ticker = self.spotAPI.get_specific_ticker(self.spot_ID)
                # 公共-获取合约ticker信息
                # swap_ticker = self.swapAPI.get_specific_ticker(self.swap_ID)
                tickers = self.parallel_ticker()
                spot_ticker = tickers[0]
                swap_ticker = tickers[1]
                # 现货最高卖出价
                best_bid = float(spot_ticker['best_bid'])
                # 合约最低买入价
                best_ask = float(swap_ticker['best_ask'])

                # 如果不满足期现溢价
                if best_ask > best_bid * (1 + price_diff):
                    # print("当前期现差价: ", (best_ask - best_bid) / best_bid, ">", price_diff)
                    counter = 0
                    time.sleep(SLEEP)
                # 监视溢价持久度
                else:
                    if counter < CONFIRMATION:
                        counter += 1
                        time.sleep(SLEEP)
                    else:
                        if target_position > spot_position:
                            fprint(insufficient_spot)
                            break
                        elif target_position > swap_position:
                            fprint(insufficient_margin)
                            break
                        else:
                            # 计算下单数量
                            best_bid_size = float(spot_ticker['best_bid_size'])
                            best_ask_size = float(swap_ticker['best_ask_size'])
                            order_size = min(target_position, round_to(best_bid_size, min_size),
                                             best_ask_size * contract_val)
                            order_size = round_to(order_size, contract_val)
                            # print(order_size)
                            contract_size = round(order_size / contract_val)
                            spot_size = round_to(order_size, size_increment)
                            # print(contract_size, spot_size, min_size)

                            # 下单
                            if order_size > 0:
                                try:
                                    # 现货下单（Fill or Kill）
                                    kwargs = {'instrument_id': self.spot_ID, 'side': 'sell', 'size': str(spot_size),
                                              'price': best_bid, 'order_type': '2'}
                                    thread1 = MyThread(target=self.spotAPI.take_order, kwargs=kwargs)
                                    thread1.start()

                                    # 合约下单（Fill or Kill）
                                    kwargs = {'instrument_id': self.swap_ID, 'type': '4', 'size': str(contract_size),
                                              'price': best_ask, 'order_type': '2'}
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
                                                # 市价平空合约
                                                swap_order = self.swapAPI.take_order(instrument_id=self.swap_ID,
                                                                                     type='4',
                                                                                     size=str(contract_size), price='',
                                                                                     order_type='4')
                                            except Exception as e:
                                                fprint(e)
                                                return 0
                                        else:
                                            fprint("swap_order_state", swap_order_state)
                                            fprint(await_status_update)
                                    elif swap_order_state == '2':
                                        if spot_order_state in ['-1', '-2']:
                                            fprint(spot_order_retract, spot_order_state)
                                            try:
                                                # 市价卖出现货
                                                spot_order = self.spotAPI.take_order(instrument_id=self.spot_ID,
                                                                                     side='sell', size=str(spot_size),
                                                                                     type='market')
                                            except Exception as e:
                                                fprint(e)
                                                return 0
                                        else:
                                            fprint("spot_order_state", spot_order_state)
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
                                        fprint(reduced_amount, filled_sum, self.coin)
                                        if usdt_release != 0:
                                            if self.transfer_from_spot(usdt_release):
                                                fprint(spot_recoup, usdt_release, "USDT")
                                        return usdt_release

                                if spot_order_state == '2' and swap_order_state == '2':
                                    usdt_release += float(spot_order_info['filled_notional']) + float(
                                        spot_order_info['fee'])
                                    spot_filled = float(spot_order_info['filled_size'])
                                    swap_filled = float(swap_order_info['filled_qty']) * contract_val
                                    filled_sum += swap_filled
                                    fee_total += float(spot_order_info['fee'])
                                    spot_notional += float(spot_order_info['filled_notional'])
                                    fee_total += float(swap_order_info['fee'])
                                    swap_price = float(swap_order_info['price_avg'])
                                    swap_notional -= swap_filled * swap_price
                                    if abs(spot_filled - swap_filled) < contract_val:
                                        target_position -= swap_filled
                                        fprint(hedge_success, swap_filled, remaining + str(target_position))
                                    else:
                                        fprint(hedge_fail)
                                        break

                                spot_position = self.spot_position()
                                swap_position = self.swap_position()
                                target_position = min(target_position, spot_position, swap_position)
                                counter = 0
                            else:
                                # print("订单太小", order_size)
                                time.sleep(SLEEP)
            if spot_notional != 0:
                Ledger = record.Record('Ledger')
                timestamp = datetime.utcnow()
                mylist = []
                mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "现货卖出",
                          'spot_notional': spot_notional}
                mylist.append(mydict)
                mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "合约平空",
                          'swap_notional': swap_notional}
                mylist.append(mydict)
                mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "手续费",
                          'fee': fee_total}
                mylist.append(mydict)
                Ledger.mycol.insert_many(mylist)
            fprint(reduced_amount, filled_sum, self.coin)
            if usdt_release != 0:
                if self.transfer_from_spot(usdt_release):
                    fprint(spot_recoup, usdt_release, "USDT")
            mydict = {'account': self.accountid, 'instrument': self.coin, 'op': 'reduce'}
            OP.mycol.delete_one(mydict)
            return usdt_release

    def close(self, price_diff=0.002, accelerate_after=0):
        """平仓期现组合

        :param price_diff: 期现差价
        :param accelerate_after: 几小时后加速
        :return: 平仓所得USDT
        :rtype: float
        """
        min_size = float(self.spot_info['min_size'])
        size_increment = float(self.spot_info['size_increment'])
        contract_val = float(self.swap_info['contract_val'])

        spot_position = self.spot_position()
        swap_position = self.swap_position()
        target_position = min(spot_position, swap_position)

        fprint(self.coin, amount_to_close, target_position)
        OP = record.Record('OP')
        mydict = {'account': self.accountid, 'instrument': self.coin, 'op': 'close'}
        OP.mycol.insert_one(mydict)

        counter = 0
        filled_sum = 0.
        usdt_release = 0.
        fee_total = 0.
        spot_notional = 0.
        swap_notional = 0.
        time_to_accelerate = datetime.utcnow() + timedelta(hours=accelerate_after)
        Stat = trading_data.Stat(self.coin)
        # 如果仍未减仓完毕
        while target_position > 0 and not self.exitFlag:
            # 判断是否加速
            if accelerate_after and datetime.utcnow() > time_to_accelerate:
                recent = Stat.recent_close_stat(accelerate_after)
                price_diff = recent['avg'] - 2 * recent['std']
                time_to_accelerate = datetime.utcnow() + timedelta(hours=accelerate_after)

            # 公共-获取现货ticker信息
            # spot_ticker = self.spotAPI.get_specific_ticker(self.spot_ID)
            # 公共-获取合约ticker信息
            # swap_ticker = self.swapAPI.get_specific_ticker(self.swap_ID)
            tickers = self.parallel_ticker()
            spot_ticker = tickers[0]
            swap_ticker = tickers[1]
            # 现货最高卖出价
            best_bid = float(spot_ticker['best_bid'])
            # 合约最低买入价
            best_ask = float(swap_ticker['best_ask'])

            # 如果不满足期现溢价
            if best_ask > best_bid * (1 + price_diff):
                # print("当前期现差价: ", (best_ask - best_bid) / best_bid, ">", price_diff)
                counter = 0
                time.sleep(SLEEP)
            # 监视溢价持久度
            else:
                if counter < CONFIRMATION:
                    counter += 1
                    time.sleep(SLEEP)
                else:
                    if target_position > spot_position:
                        fprint(insufficient_spot)
                        break
                    elif target_position > swap_position:
                        fprint(insufficient_swap)
                        break
                    else:
                        # 计算下单数量
                        best_bid_size = float(spot_ticker['best_bid_size'])
                        best_ask_size = float(swap_ticker['best_ask_size'])

                        if target_position < swap_position:  # spot=target=1.9 swap=2.0
                            order_size = min(target_position, round_to(best_bid_size, min_size),
                                             best_ask_size * contract_val)  # order=1.9 or 1, 44
                            contract_size = round(order_size / contract_val)  # 2 or 1, 40
                            spot_size = round_to(order_size, size_increment)  # 1.9 or 1, 44
                            remnant = (spot_position - spot_size) / min_size
                            # print(order_size, contract_size, spot_size, remnant)
                            # 必须一次把现货出完
                            if remnant >= 1:
                                order_size = contract_size * contract_val
                                spot_size = round_to(order_size, size_increment)
                            elif round(remnant) > 0 and remnant < 1:  # 1.9-1=0.9<1
                                time.sleep(SLEEP)
                                continue
                            else:  # 1.9-1.9=0
                                pass
                        else:  # spot=2.1 swap=target=2.0
                            order_size = min(target_position, round_to(best_bid_size, min_size),
                                             best_ask_size * contract_val)  # order=2 or 1, 1.5
                            contract_size = round(order_size / contract_val)  # 2 or 1
                            spot_size = round_to(order_size, size_increment)  # 2 or 1, 1.5
                            remnant = (spot_position - spot_size) / min_size
                            # 必须一次把现货出完
                            if remnant >= 1:  # 2.1-1>1
                                order_size = contract_size * contract_val
                                spot_size = round_to(order_size, size_increment)
                            elif remnant < 1:  # 2.1-2=0.1
                                if spot_position <= best_bid_size:  # 2.1<3
                                    spot_size = spot_position  # 2->2.1
                                else:
                                    time.sleep(SLEEP)
                                    continue
                        # 下单
                        if order_size > 0:
                            try:
                                # 现货下单（Fill or Kill）
                                kwargs = {'instrument_id': self.spot_ID, 'side': 'sell', 'size': str(spot_size),
                                          'price': best_bid, 'order_type': '2'}
                                thread1 = MyThread(target=self.spotAPI.take_order, kwargs=kwargs)
                                thread1.start()

                                # 合约下单（Fill or Kill）
                                kwargs = {'instrument_id': self.swap_ID, 'type': '4', 'size': str(contract_size),
                                          'price': best_ask, 'order_type': '2'}
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
                                            # 市价平空合约
                                            swap_order = self.swapAPI.take_order(instrument_id=self.swap_ID, type='4',
                                                                                 size=str(contract_size), price='',
                                                                                 order_type='4')
                                        except Exception as e:
                                            fprint(e)
                                            return 0
                                    else:
                                        fprint("swap_order_state", swap_order_state)
                                        fprint(await_status_update)
                                elif swap_order_state == '2':
                                    if spot_order_state in ['-1', '-2']:
                                        fprint(spot_order_retract, spot_order_state)
                                        try:
                                            # 市价卖出现货
                                            spot_order = self.spotAPI.take_order(instrument_id=self.spot_ID,
                                                                                 side='sell', size=str(spot_size),
                                                                                 type='market')
                                        except Exception as e:
                                            fprint(e)
                                            return 0
                                    else:
                                        fprint("spot_order_state", spot_order_state)
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
                                    fprint(reduced_amount, filled_sum, self.coin)
                                    return usdt_release

                            if spot_order_state == '2' and swap_order_state == '2':
                                usdt_release += float(spot_order_info['filled_notional']) + float(
                                    spot_order_info['fee'])
                                spot_filled = float(spot_order_info['filled_size'])
                                swap_filled = float(swap_order_info['filled_qty']) * contract_val
                                filled_sum += swap_filled
                                fee_total += float(spot_order_info['fee'])
                                spot_notional += float(spot_order_info['filled_notional'])
                                fee_total += float(swap_order_info['fee'])
                                swap_price = float(swap_order_info['price_avg'])
                                swap_notional -= swap_filled * swap_price
                                if abs(spot_filled - swap_filled) < contract_val:
                                    target_position -= swap_filled
                                    fprint(hedge_success, swap_filled, remaining + str(target_position))
                                else:
                                    fprint(hedge_fail)
                                    break

                            spot_position = self.spot_position()
                            swap_position = self.swap_position()
                            target_position = min(target_position, spot_position, swap_position)
                            counter = 0
                        else:
                            # print("订单太小", order_size)
                            time.sleep(SLEEP)
        if spot_notional != 0:
            Ledger = record.Record('Ledger')
            timestamp = datetime.utcnow()
            mylist = []
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "现货卖出",
                      'spot_notional': spot_notional}
            mylist.append(mydict)
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "合约平空",
                      'swap_notional': swap_notional}
            mylist.append(mydict)
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "手续费",
                      'fee': fee_total}
            mylist.append(mydict)
            mydict = {'account': self.accountid, 'instrument': self.coin, 'timestamp': timestamp, 'title': "平仓"}
            mylist.append(mydict)
            Ledger.mycol.insert_many(mylist)
        fprint(closed_amount, filled_sum, self.coin)
        swap_balance = self.swap_balance()
        usdt_release += swap_balance
        if usdt_release != 0:
            if self.transfer_to_spot(swap_balance):
                fprint(spot_recoup, usdt_release, "USDT")
        mydict = {'account': self.accountid, 'instrument': self.coin, 'op': 'close'}
        OP.mycol.delete_one(mydict)
        return usdt_release
