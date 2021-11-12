import okex.account_api as account
import okex.spot_api as spot
import okex.swap_api as swap
from okex.exceptions import OkexAPIException
import key
import time
from mythread import MyThread
from log import fprint
from lang import *

SLEEP = 0.2
CONFIRMATION = 3


def round_to(number, fraction):
    """返回fraction的倍数
    """
    # 小数点后位数
    ndigits = len('{:f}'.format(fraction - int(fraction))) - 2
    if ndigits > 0:
        return round(int(number / fraction) * fraction, ndigits)
    else:
        return round(int(number / fraction) * fraction)


class OKExAPI:
    """基本OKEx功能类
    """

    def __init__(self, coin, accountid):
        self.accountid = accountid
        apikey = key.Key(accountid)
        api_key = apikey.api_key
        secret_key = apikey.secret_key
        passphrase = apikey.passphrase

        if accountid == 3:
            self.accountAPI = account.AccountAPI(api_key, secret_key, passphrase, test=True)
            self.spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, test=True)
            self.swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, test=True)
        else:
            self.accountAPI = account.AccountAPI(api_key, secret_key, passphrase, False)
            self.spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
            self.swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)

        self.coin = coin
        self.spot_ID = coin + '-USDT'
        self.swap_ID = coin + '-USDT-SWAP'

        self.exitFlag = False
        self.exist = True

        # 公共-获取现货信息
        self.spot_info = self.spotAPI.get_instrument(self.spot_ID)

        # 公共-获取合约信息
        self.swap_info = self.swapAPI.get_instrument(self.swap_ID)
        if not self.swap_info:
            fprint(nonexistent_crypto)
            self.exist = False
            del self

    def usdt_balance(self):
        """获取USDT现货
        """
        return float(self.spotAPI.get_coin_account_info('USDT')['available'])

    def spot_position(self):
        """获取现货仓位
        """
        return float(self.spotAPI.get_coin_account_info(self.coin)['available'])

    def swap_holding(self):
        """获取合约持仓
        """
        holding = {}
        for n in self.swapAPI.get_specific_position(self.swap_ID)['holding']:
            if n['side'] == 'short':
                # print(n)
                holding = n
        return holding

    def swap_position(self):
        """获取合约仓位
        """
        contract_val = float(self.swap_info['contract_val'])
        holding = self.swap_holding()
        if holding:
            return float(holding['avail_position']) * contract_val
        else:
            return 0.

    def swap_margin(self):
        """获取合约占用保证金
        """
        swap_account = self.swapAPI.get_coin_account(self.swap_ID)['info']
        return float(swap_account['equity'])

    def swap_balance(self):
        """获取可用保证金
        """
        swap_account = self.swapAPI.get_coin_account(self.swap_ID)['info']
        return float(swap_account['max_withdraw'])

    def get_lever(self):
        setting = self.swapAPI.get_settings(self.swap_ID)
        return int(float(setting['short_leverage']))

    def transfer_to_spot(self, transfer_amount=0.):
        """划转USDT到现货账户

        :param transfer_amount: 划转金额
        :return: 是否成功
        :rtype: bool
        """
        if transfer_amount <= 0:
            return False
        try:
            transfer = self.accountAPI.coin_transfer(currency='USDT', amount=str(transfer_amount),
                                                     account_from='9', account_to='1', instrument_id=self.spot_ID,
                                                     to_instrument_id='')
            if transfer['result']:
                fprint(transfer_text + str(transfer_amount) + "USDT" + to_spot_account)
                return True
            else:
                fprint(transfer_failed)
                return False
        except OkexAPIException as e:
            fprint(e)
            fprint(transfer_failed)
            if e.code == "58110":
                time.sleep(600)
            return False

    def transfer_from_spot(self, transfer_amount=0.):
        """从现货账户划转USDT

        :param transfer_amount: 划转金额
        :return: 是否成功
        :rtype: bool
        """
        if transfer_amount <= 0:
            return False
        try:
            transfer = self.accountAPI.coin_transfer(currency='USDT', amount=str(transfer_amount),
                                                     account_from='1', account_to='9', instrument_id='',
                                                     to_instrument_id=self.spot_ID)
            if transfer['result']:
                fprint(transfer_text + str(transfer_amount) + "USDT" + to_swap_account)
                return True
            else:
                fprint(transfer_failed)
                return False
        except OkexAPIException as e:
            fprint(e)
            fprint(transfer_failed)
            return False

    def parallel_ticker(self):
        """多线程获取现货合约价格
        """
        # 最小延时0.34
        # send = time.time()
        thread1 = MyThread(target=self.spotAPI.get_specific_ticker, args=(self.spot_ID,))
        thread1.start()
        thread2 = MyThread(target=self.swapAPI.get_specific_ticker, args=(self.swap_ID,))
        thread2.start()
        thread1.join()
        thread2.join()
        spot_ticker = thread1.get_result()
        swap_ticker = thread2.get_result()
        # receive = time.time()
        # if receive - send > 0.2:
        #     print("timeout", receive - send)
        del thread1
        del thread2
        return [spot_ticker, swap_ticker]
