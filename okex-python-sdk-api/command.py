from datetime import timezone
import funding_rate
import monitor
import open_position
import close_position
import trading_data
import record
import threading
import multiprocessing
from log import fprint


# 监控
def monitor_all(accountid=2):
    processes = []
    fundingRate = funding_rate.FundingRate()
    for n in get_coinlist(accountid):
        mon = monitor.Monitor(coin=n, accountid=accountid)
        process = multiprocessing.Process(target=mon.watch)
        process.start()
        processes.append(process)

        current_rate = fundingRate.current(mon.swap_ID)
        next_rate = fundingRate.next(mon.swap_ID)
        fprint("{}当期资金费{:.3%}, 预测资金费{:.3%}".format(mon.coin, current_rate, next_rate))
        fprint("{:6s}今日APR: {:.2%}，7日APR: {:.2%}".format(n, mon.apr(1), mon.apr(7)))
        fprint("{:6s}今日APY: {:.2%}，7日APY: {:.2%}".format(n, mon.apy(1), mon.apy(7)))
    for n in processes:
        n.join()


# 收益统计
def profit_all(accountid=2):
    for coin in get_coinlist(accountid):
        mon = monitor.Monitor(coin=coin, accountid=accountid)
        fprint("{:6s}今日APY: {:.2%}，7日APY: {:.2%}, 累计APY: {:.2%}".format(coin, mon.apy(1), mon.apy(7), mon.apy()))
        Stat = trading_data.Stat(coin)
        funding = Stat.history_funding(accountid)
        cost = Stat.history_cost(accountid)
        localtime = Stat.open_time(accountid).replace(tzinfo=timezone.utc).astimezone().replace(tzinfo=None)
        fprint("开仓时间: {}，累计收益: {:.2f} USDT".format(localtime.isoformat(timespec='minutes'), funding + cost))


# 补录资金费
def back_track_all(accountid=2):
    processes = []
    for n in get_coinlist(accountid):
        mon = monitor.Monitor(coin=n, accountid=accountid)
        process = multiprocessing.Process(target=mon.back_tracking)
        process.start()
        processes.append(process)
    for n in processes:
        n.join()


# 平仓
def close_all(accountid=2):
    fundingRate = funding_rate.FundingRate()
    processes = []
    for n in get_coinlist(accountid):
        mon = monitor.Monitor(coin=n, accountid=accountid)
        if not mon.position_exist():
            continue
        stat = trading_data.Stat(coin=n)
        reducePosition = close_position.ReducePosition(coin=n, accountid=accountid)
        recent = stat.recent_close_stat(4)
        close_pd = recent['avg'] - 2 * recent['std']
        fprint("{:6s} Funding Rate: {:7.3%}, Close Avg: {:7.3%}, Std: {:7.3%}, Min: {:7.3%}, 2 Sigma: {:7.3%}"
               .format(n, fundingRate.current(n + '-USDT-SWAP'), recent['avg'], recent['std'], recent['min'], close_pd))
        process = multiprocessing.Process(target=reducePosition.close, args=(close_pd, 2))
        process.start()
        processes.append(process)
    for n in processes:
        n.join()


# 当前持仓币种
def get_coinlist(account=2):
    Record = record.Record('Ledger')
    pipeline = [
        {
            '$match': {
                'account': account
            }
        }, {
            '$group': {
                '_id': '$instrument'
            }
        }
    ]
    temp = []
    result = []
    for x in Record.mycol.aggregate(pipeline):
        temp.append(x['_id'])
    for n in temp:
        mon = monitor.Monitor(coin=n, accountid=account)
        if not mon.position_exist():
            continue
        result.append(n)
    return result


def get_command(account=1):
    command = input(main_menu)
    while command != 'q':
        if command == '1':
            thread = threading.Thread(target=record.record_ticker)
            thread.start()
            monitor_all(account)
        elif command == '2':
            coin = input("输入操作币种\n")
            Monitor = monitor.Monitor(coin=coin, accountid=account)
            if Monitor.exist:
                command = input(coin_menu)
            else:
                continue
            if command == '1':
                usdt = float(input("输入USDT数量\n"))
                AddPosition = open_position.AddPosition(coin=coin, accountid=account)
                hours = 2
                Stat = trading_data.Stat(coin)
                recent = Stat.recent_open_stat(hours)
                open_pd = recent['avg'] + 2 * recent['std']
                AddPosition.open(usdt_size=usdt, leverage=3, price_diff=open_pd, accelerate_after=hours)
                if AddPosition.is_hedged():
                    fprint(coin, "成功对冲")
                else:
                    fprint(coin, "对冲失败，需手动检查")
            elif command == '2':
                usdt = float(input("输入USDT数量\n"))
                ReducePosition = close_position.ReducePosition(coin=coin, accountid=account)
                hours = 2
                Stat = trading_data.Stat(coin)
                recent = Stat.recent_close_stat(hours)
                close_pd = recent['avg'] - 2 * recent['std']
                ReducePosition.reduce(usdt_size=usdt, price_diff=close_pd, accelerate_after=hours)
            elif command == '3':
                ReducePosition = close_position.ReducePosition(coin=coin, accountid=account)
                hours = 2
                Stat = trading_data.Stat(coin)
                recent = Stat.recent_close_stat(hours)
                close_pd = recent['avg'] - 2 * recent['std']
                ReducePosition.close(price_diff=close_pd, accelerate_after=hours)
            elif command == '4':
                if not Monitor.position_exist():
                    fprint("没有仓位")
                else:
                    fprint("{:6s}今日APY: {:.2%}，7日APY: {:.2%}, 累计APY: {:.2%}".format(coin, Monitor.apy(1), Monitor.apy(7),
                                                                                    Monitor.apy()))
                    Stat = trading_data.Stat(coin)
                    funding = Stat.history_funding(account)
                    cost = Stat.history_cost(account)
                    localtime = Stat.open_time(account).replace(tzinfo=timezone.utc).astimezone().replace(
                        tzinfo=None)
                    fprint("开仓时间: {}，累计收益: {:.2f} USDT".format(localtime.isoformat(timespec='minutes'),
                                                               funding + cost))
            elif command == 'b':
                pass
            else:
                print("错误指令")
        elif command == '3':
            FundingRate = funding_rate.FundingRate()
            command = input(funding_menu)
            while command != 'b':
                if command == '1':
                    days = int(input("统计最近几天？\n"))
                    FundingRate.show_profitable_rate(days)
                elif command == '2':
                    FundingRate.show_selected_rate(get_coinlist(account))
                elif command == '3':
                    FundingRate.show_7day_rate()
                elif command == '4':
                    FundingRate.show_30day_rate()
                elif command == 'b':
                    break
                else:
                    print("错误指令")
                command = input(funding_menu)
        elif command == '4':
            command = input(account_menu)
            while command != 'b':
                if command == '1':
                    back_track_all(accountid=account)
                elif command == '2':
                    profit_all(accountid=account)
                elif command == '3':
                    coin = input("输入币种\n")
                    Stat = trading_data.Stat(coin)
                    if Stat.exist:
                        hours = int(input("输入时长\n"))
                        Stat.plot(hours)
                    else:
                        continue
                elif command == 'b':
                    break
                else:
                    print("错误指令")
                command = input(account_menu)
        elif command == 'q':
            exit()
        else:
            print("错误指令")
        command = input(main_menu)


main_menu = """
1   监控现有仓位
2   单一币种操作
3   资金费数据
4   账户数据
q   退出
"""

coin_menu = """
1   加仓
2   减仓
3   平仓
4   收益统计
b   返回
"""

funding_menu = """
1   显示收益最高十个币种
2   显示持仓币种当前资金费
3   显示全币种最近7天资金费
4   显示全币种最近30天资金费
b   返回
"""

account_menu = """
1   补录资金费
2   持仓币种收益统计
3   期现差价统计
b   返回
"""
