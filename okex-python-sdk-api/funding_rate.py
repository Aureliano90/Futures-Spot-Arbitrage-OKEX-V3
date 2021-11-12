from typing import List
import okex.swap_api as swap
import statistics
import record
import trading_data
from log import fprint
from lang import *


class FundingRate:

    def __init__(self):
        self.swapAPI = swap.SwapAPI(api_key='', api_secret_key='', passphrase='')

    def get_instruments(self):
        """获取合约币种列表

        :rtype: List[str]
        """
        instruments = self.swapAPI.get_instruments()
        # pprint(instruments)
        instrumentsID = []  # 空列表
        for n in instruments:
            if n['instrument_id'].find('USDT') != -1:  # 只统计U本位合约
                instrumentsID.append(n['instrument_id'])
        # print(instrumentsID)
        return instrumentsID

    def current(self, instrument_id=''):
        """当期资金费

        :param instrument_id: 币种合约
        """
        current_rate = self.swapAPI.get_funding_time(instrument_id=instrument_id)['funding_rate']
        if current_rate:
            current_rate = float(current_rate)
        else:
            # print(instrument_id, current_rate)
            current_rate = 0
        return current_rate

    def next(self, instrument_id=''):
        """预测资金费

        :param instrument_id: 币种合约
        """
        next_rate = self.swapAPI.get_funding_time(instrument_id=instrument_id)['estimated_rate']
        if next_rate:
            next_rate = float(next_rate)
        else:
            # print(instrument_id, next_rate)
            next_rate = 0
        return next_rate

    def show_current_rate(self):
        """显示当前资金费
        """
        instrumentsID = self.get_instruments()

        funding_rate_list = []
        for m in instrumentsID:
            current_funding_rate = self.swapAPI.get_funding_time(instrument_id=m)
            if current_funding_rate['funding_rate']:
                current_rate = float(current_funding_rate['funding_rate'])
            else:
                current_rate = 0
            if current_funding_rate['estimated_rate']:
                estimated_rate = float(current_funding_rate['estimated_rate'])
            else:
                estimated_rate = 0
            funding_rate_list.append(
                {'instrument_id': m, 'current_rate': current_rate, 'estimated_rate': estimated_rate})
        funding_rate_list.sort(key=lambda x: x['current_rate'], reverse=True)
        # pprint(funding_rate_list)
        fprint(coin_current_next)
        for n in funding_rate_list:
            instrumentID = n['instrument_id'][:n['instrument_id'].find('-')]
            current_rate = n['current_rate']
            estimated_rate = n['estimated_rate']
            fprint('{:6s}{:9.3%}{:11.3%}'.format(instrumentID, current_rate, estimated_rate))

    def show_7day_rate(self):
        """显示最近7天平均资金费
        """
        instrumentsID = self.get_instruments()

        funding_rate_list = []
        for m in instrumentsID:
            realized_rate = []
            historical_funding_rate = self.swapAPI.get_historical_funding_rate(instrument_id=m, limit='21')
            # pprint(historical_funding_rate)
            # 永续合约上线不一定有30天
            if len(historical_funding_rate) == 0:
                # print(m + "还没有数据。")
                pass
            elif len(historical_funding_rate) < 21:
                # print(m + "上线不到7天。")
                pass
            else:
                for n in historical_funding_rate:
                    realized_rate.append(float(n['realized_rate']))
                funding_rate_list.append({'instrument_id': m, '7day_funding_rate': statistics.mean(realized_rate[:21])})

        funding_rate_list.sort(key=lambda x: x['7day_funding_rate'], reverse=True)
        # 打印历史资金费
        # pprint(funding_rate_list)
        fprint(funding_7day)
        for n in funding_rate_list:
            instrumentID = n['instrument_id'][:n['instrument_id'].find('-')]
            fprint('{:8s}{:8.3%}'.format(instrumentID, n['7day_funding_rate']))

    def show_30day_rate(self):
        """显示最近30天平均资金费
        """
        instrumentsID = self.get_instruments()

        funding_rate_list = []
        for m in instrumentsID:
            realized_rate = []
            historical_funding_rate = self.swapAPI.get_historical_funding_rate(instrument_id=m, limit='90')
            # pprint(historical_funding_rate)
            # 永续合约上线不一定有30天
            if len(historical_funding_rate) == 0:
                # print(m + "还没有数据。")
                pass
            elif len(historical_funding_rate) < 90:
                # print(m + "上线不到30天。")
                pass
            else:
                for n in historical_funding_rate:
                    realized_rate.append(float(n['realized_rate']))
                funding_rate_list.append(
                    {'instrument_id': m, '30day_funding_rate': statistics.mean(realized_rate[:90])})

        funding_rate_list.sort(key=lambda x: x['30day_funding_rate'], reverse=True)
        # 打印历史资金费
        # pprint(funding_rate_list)
        fprint(funding_30day)
        for n in funding_rate_list:
            instrumentID = n['instrument_id'][:n['instrument_id'].find('-')]
            fprint('{:8s}{:8.3%}'.format(instrumentID, n['30day_funding_rate']))

    def print_30day_rate(self):
        """输出最近30天平均资金费到文件
        """
        instrumentsID = self.get_instruments()

        funding_rate_list = []
        for m in instrumentsID:
            realized_rate = []
            historical_funding_rate = self.swapAPI.get_historical_funding_rate(instrument_id=m, limit='90')
            # pprint(historical_funding_rate)
            # 永续合约上线不一定有30天
            if len(historical_funding_rate) < 21:
                # print(m + "上线不到7天。")
                pass
            elif len(historical_funding_rate) < 90:
                # print(m + "上线不到30天。")
                for n in historical_funding_rate:
                    realized_rate.append(float(n['realized_rate']))
                funding_rate_list.append({'instrument_id': m, '7day_funding_rate': statistics.mean(realized_rate[:21]),
                                          '30day_funding_rate': 0})
            else:
                for n in historical_funding_rate:
                    realized_rate.append(float(n['realized_rate']))
                funding_rate_list.append({'instrument_id': m, '7day_funding_rate': statistics.mean(realized_rate[:21]),
                                          '30day_funding_rate': statistics.mean(realized_rate[:90])})

        funding_rate_list.sort(key=lambda x: x['30day_funding_rate'], reverse=True)
        funding_rate_list.sort(key=lambda x: x['7day_funding_rate'], reverse=True)

        funding_rate_file = open("Funding Rate.txt", "w", encoding="utf-8")
        funding_rate_file.write(coin_7_30)
        for n in funding_rate_list:
            instrumentID = n['instrument_id'][:n['instrument_id'].find('-')]
            funding_rate_file.write(instrumentID.ljust(7))
            funding_rate_file.write('{:7.3%}'.format(n['7day_funding_rate']))
            funding_rate_file.write('{:8.3%}'.format(n['30day_funding_rate']) + '\n')
        funding_rate_file.close()

    def get_rate(self, days=7):
        """返回最近资金费列表

        :param days: 最近几天
        :rtype: List[dict]
        """
        instrumentsID = self.get_instruments()
        limit = str(days * 3)

        funding_rate_list = []
        for m in instrumentsID:
            realized_rate = []
            historical_funding_rate = self.swapAPI.get_historical_funding_rate(instrument_id=m, limit=limit)
            if len(historical_funding_rate) < days * 3:
                pass
            else:
                instrumentID = m[:m.find('-')]
                for n in historical_funding_rate:
                    realized_rate.append(float(n['realized_rate']))
                funding_rate_list.append({'instrument': instrumentID, 'funding_rate': statistics.mean(realized_rate)})
        return funding_rate_list

    def store(self):
        """补录最近30天资金费率
        """
        Record = record.Record('Funding')
        instrumentsID = self.get_instruments()
        found, inserted = 0, 0

        for m in instrumentsID:
            instrumentID = m[:m.find('-')]
            historical_funding_rate = self.swapAPI.get_historical_funding_rate(instrument_id=m)
            found += len(historical_funding_rate)
            for n in historical_funding_rate:
                timestamp = record.fromiso8601(n['funding_time'])
                myquery = {'instrument': instrumentID, 'timestamp': timestamp}
                mydict = {'instrument': instrumentID, 'timestamp': timestamp, 'funding': float(n['realized_rate'])}
                # 查重
                if not Record.mycol.find_one(myquery):
                    Record.mycol.insert_one(mydict)
                    inserted += 1
        print("Found: {}, Inserted: {}".format(found, inserted))

    def show_profitable_rate(self, days=7):
        """显示收益最高十个币种资金费
        """
        funding_rate_list = trading_data.profitability(days)
        for m in funding_rate_list:
            funding_rate: dict = self.swapAPI.get_funding_time(m['instrument']+'-USDT-SWAP')
            if funding_rate['funding_rate']:
                current_rate = float(funding_rate['funding_rate'])
            else:
                current_rate = 0
            if funding_rate['estimated_rate']:
                estimated_rate = float(funding_rate['estimated_rate'])
            else:
                estimated_rate = 0
            m['current_rate'] = current_rate
            m['estimated_rate'] = estimated_rate
        funding_rate_list.sort(key=lambda x: x['current_rate'], reverse=True)
        # pprint(funding_rate_list)
        fprint(coin_current_next)
        for n in funding_rate_list:
            instrumentID = n['instrument']
            current_rate = n['current_rate']
            estimated_rate = n['estimated_rate']
            fprint('{:6s}{:9.3%}{:11.3%}'.format(instrumentID, current_rate, estimated_rate))

    def show_selected_rate(self, coinlist: list):
        """显示列表币种当前资金费

        :param coinlist:
        """
        funding_rate_list = [{'instrument': n} for n in coinlist]
        for m in funding_rate_list:
            funding_rate: dict = self.swapAPI.get_funding_time(m['instrument']+'-USDT-SWAP')
            if funding_rate['funding_rate']:
                current_rate = float(funding_rate['funding_rate'])
            else:
                current_rate = 0
            if funding_rate['estimated_rate']:
                estimated_rate = float(funding_rate['estimated_rate'])
            else:
                estimated_rate = 0
            m['current_rate'] = current_rate
            m['estimated_rate'] = estimated_rate
        funding_rate_list.sort(key=lambda x: x['current_rate'], reverse=True)
        # pprint(funding_rate_list)
        fprint(coin_current_next)
        for n in funding_rate_list:
            instrumentID = n['instrument']
            current_rate = n['current_rate']
            estimated_rate = n['estimated_rate']
            fprint('{:6s}{:9.3%}{:11.3%}'.format(instrumentID, current_rate, estimated_rate))
