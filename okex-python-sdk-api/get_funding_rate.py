import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import okex.information_api as information
import key
import json
import datetime
import time
import statistics
from pprint import pprint

if __name__ == '__main__':

    api_key = key.api_key
    secret_key = key.secret_key
    passphrase = key.passphrase

    swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)

    # 获取合约币种列表
    instruments = swapAPI.get_instruments()
    # pprint(instruments)
    instrumentsID = []  # 空列表
    for n in range(len(instruments)):
        if instruments[n]['instrument_id'].find('USDT') != -1: #只统计U本位合约
            instrumentsID.append(instruments[n]['instrument_id'])
    # print(instrumentsID)

    # 公共-获取合约资金费率
    funding_rate_list = []
    for m in range(len(instrumentsID)):
        current_funding_rate = swapAPI.get_funding_time(instrument_id=instrumentsID[m])
        if current_funding_rate['funding_rate']:
            current_funding_rate['funding_rate'] = float(current_funding_rate['funding_rate'])
        else:
            # print(instrumentsID[m], current_funding_rate['funding_rate'] )
            current_funding_rate['funding_rate'] = 0
        if current_funding_rate['estimated_rate']:
            current_funding_rate['estimated_rate'] = float(current_funding_rate['estimated_rate'])
        else:
            current_funding_rate['estimated_rate'] = 0
        expected_rate = 0.5 * (current_funding_rate['funding_rate'] + current_funding_rate['estimated_rate'])
        expected_rate = '{:.5f}'.format(expected_rate)
        funding_rate_list.append({'instrument_id': instrumentsID[m], 'expected_rate': expected_rate})
        if m > 0 and m % 20 == 0:
            time.sleep(1.5)
    funding_rate_list.sort(key=lambda x: float(x['expected_rate']), reverse=True)
    # pprint(funding_rate_list)
    print(("币种   预期资金费"))
    for m in range(len(funding_rate_list)):
        instrumentID = funding_rate_list[m]['instrument_id'][:funding_rate_list[m]['instrument_id'].find('-')]
        print(instrumentID.ljust(7),end='')
        print(funding_rate_list[m]['expected_rate'].ljust(10))

    # 公共-获取合约历史资金费率
    # historical_funding_rate = swapAPI.get_historical_funding_rate(instrument_id='MIR-USDT-SWAP', limit='90')
    # print(len(historical_funding_rate))

    funding_rate_list = []
    for m in range(len(instrumentsID)):
        realized_rate = []
        historical_funding_rate = swapAPI.get_historical_funding_rate(instrument_id=instrumentsID[m], limit='90')
        # pprint(historical_funding_rate)
        # 永续合约上线不一定有30天
        if len(historical_funding_rate) ==0 :
            print(instrumentsID[m]+"还没有数据。")
        else:
            for n in range(len(historical_funding_rate)):
                realized_rate.append(float(historical_funding_rate[n]['realized_rate']))
            funding_rate_list.append(
                {'instrument_id': instrumentsID[m], '7day_funding_rate': '{:.5f}'.format(statistics.mean(realized_rate[:21])),
                 '30day_funding_rate': '{:.5f}'.format(statistics.mean(realized_rate[:90]))})
        if m > 0 and m % 20 == 0:
            time.sleep(1)

    funding_rate_list.sort(key=lambda x: float(x['7day_funding_rate']), reverse=True)
    funding_rate_list.sort(key=lambda x: float(x['30day_funding_rate']), reverse=True)
    # 打印历史资金费
    # pprint(funding_rate_list)
    print(("币种   7天资金费 30天资金费"))
    for m in range(len(funding_rate_list)):
        instrumentID = funding_rate_list[m]['instrument_id'][:funding_rate_list[m]['instrument_id'].find('-')]
        print(instrumentID.ljust(7),end='')
        print(funding_rate_list[m]['7day_funding_rate'].ljust(10),end='')
        print(funding_rate_list[m]['30day_funding_rate'])

    funding_rate_file = open("Funding Rate.txt", "w")
    funding_rate_file.write("币种   7天资金费 30天资金费\n")
    for m in range(len(funding_rate_list)):
        instrumentID = funding_rate_list[m]['instrument_id'][:funding_rate_list[m]['instrument_id'].find('-')]
        funding_rate_file.write(instrumentID.ljust(7))
        funding_rate_file.write(funding_rate_list[m]['7day_funding_rate'].ljust(10))
        funding_rate_file.write(funding_rate_list[m]['30day_funding_rate']+'\n')
    funding_rate_file.close()