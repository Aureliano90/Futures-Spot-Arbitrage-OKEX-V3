import okex.spot_api as spot
import okex.swap_api as swap
import pymongo
from datetime import datetime, timedelta
import time
import funding_rate


def fromiso8601(ts: str) -> datetime:
    ts = ts[:ts.find('Z')]
    return datetime.fromisoformat(ts)


class Record:

    def __init__(self, col=''):
        self.myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        self.mydb = self.myclient['OKEx']
        self.mycol = self.mydb[col]

    def find_last(self, match: dict):
        """返回最后一条记录

        :param match: 匹配条件
        :rtype: dict
        """
        pipeline = [{
            '$match': match
        }, {
            '$sort': {
                '_id': -1
            }
        }, {
            '$limit': 1
        }
        ]
        for x in self.mycol.aggregate(pipeline):
            return x

    def delete(self):
        myquery = {
            'instrument': 'CFX',
            'title': '自动加仓',
            'timestamp': {
                '$gt': fromiso8601("2021-04-18T03:23:00.000Z")
            }}
        self.mycol.delete_many(myquery)


def record_ticker():
    ticker = Record('Ticker')
    funding = Record('Funding')
    fundingRate = funding_rate.FundingRate()
    instrumentsID = fundingRate.get_instruments()
    spotAPI = spot.SpotAPI(api_key='', api_secret_key='', passphrase='')
    swapAPI = swap.SwapAPI(api_key='', api_secret_key='', passphrase='')

    while True:
        timestamp = datetime.utcnow()
        begin = timestamp

        # 每8小时记录资金费
        if timestamp.hour % 8 == 0:
            if timestamp.minute == 1:
                if timestamp.second < 10:
                    funding_rate_list = []
                    for m in instrumentsID:
                        historical_funding_rate = fundingRate.swapAPI.get_historical_funding_rate(instrument_id=m,
                                                                                                  limit='1')
                        for n in historical_funding_rate:
                            timestamp = fromiso8601(n['funding_time'])
                            mydict = {'instrument': m[:m.find('-')], 'timestamp': timestamp,
                                      'funding': float(n['realized_rate'])}
                            funding_rate_list.append(mydict)
                    funding.mycol.insert_many(funding_rate_list)

                    myquery = {
                        'timestamp': {
                            '$lt': timestamp.__sub__(timedelta(hours=24))
                        }}
                    ticker.mycol.delete_many(myquery)

        spot_ticker = spotAPI.get_ticker()
        swap_ticker = swapAPI.get_ticker()
        mylist = []
        for m in instrumentsID:
            swap_ID = m
            spot_ID = swap_ID[:swap_ID.find('-SWAP')]
            coin = spot_ID[:spot_ID.find('-USDT')]
            spot_ask, spot_bid, swap_bid, swap_ask = 0., 0., 0., 0.
            for n in spot_ticker:
                if n['instrument_id'] == spot_ID:
                    timestamp = fromiso8601(n['timestamp'])
                    # print(timestamp)
                    spot_ask = float(n['best_ask'])
                    spot_bid = float(n['best_bid'])
            for n in swap_ticker:
                if n['instrument_id'] == swap_ID:
                    swap_ask = float(n['best_ask'])
                    swap_bid = float(n['best_bid'])
            if spot_ask and spot_bid:
                open_pd = (swap_bid - spot_ask) / spot_ask
                close_pd = (swap_ask - spot_bid) / spot_bid
            else:
                continue
            mydict = {'instrument': coin, "timestamp": timestamp, 'spot_bid': spot_bid, 'spot_ask': spot_ask,
                      'swap_bid': swap_bid, 'swap_ask': swap_ask, 'open_pd': open_pd, 'close_pd': close_pd}
            mylist.append(mydict)
        ticker.mycol.insert_many(mylist)
        timestamp = datetime.utcnow()
        delta = timestamp.__sub__(begin).total_seconds()
        if delta < 10:
            time.sleep(10 - delta)
