import requests
import json
import time
import traceback

from ngwshare.utils.date_util import str2datetime
from ngwshare.utils.http_util import get_ua
import pandas as pd
import datetime


def get_T0TradeOrder(strategy_id=None, start=None, end=None):
    split_list = strategy_id.split('.')
    symbol = split_list[0]
    exchange = 'SHSE' if split_list[0] == 'SH' else 'SZSE'
    # url = 'https://testshq.niuguwang.com/aquote/quote/Tick.ashx?startTime={}&endTime={}&symbol={}&exchange={}&limit={}'\
    #     .format(start,end,symbol,exchange,limit)
    url = 'http://192.168.3.212:6667/t0/home/Tick.ashx?startTime={}&endTime={}&symbol={}&exchange={}&limit={}' \
        .format(start, end, symbol, exchange, limit)
    try:
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        if response_json['error_no'] == 0:
            return pd.DataFrame(response_json['data'])
        else:
            return pd.DataFrame()
    except Exception:
        print(traceback.format_exc())


def GetHXL2Stock():
    try:
        url = "https://stq.niuguwang.com/zljl/GetStock"
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('resultCode') == 0:
                return response_json.get('data')
            else:
                return []
        except:
            return []


def UpdateHXL2Stock(body=None):
    try:
        url = "https://stq.niuguwang.com/zljl/RefreshStock"
        headers = {"Content-Type": "application/json", 'User-Agent': get_ua()}
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('resultCode') == 0:
                return response_json.get('data')
            else:
                return None
        except:
            return None


if __name__ == '__main__':
    t1 = time.time()


    # start = '2021-07-16 09:30:00'
    # end = '2021-07-16 15:00:00'
    # data = get_T0TradeOrder(strategy_id=13, start=start, end=end)
    # print(data)

    data = GetHXL2Stock()
    print(data)

    # stock_list = ['000651.SZ', '000995.SZ', '003040.SZ', '300144.SZ', '300339.SZ', '300397.SZ', '300598.SZ',
    #               '300722.SZ', '300727.SZ', '300981.SZ', '600519.SH', '601005.SH', '603000.SH', '600000.SH', '600436.SH']
    # data = UpdateHXL2Stock(stock_list)
    # print(data)






    print(time.time()-t1)