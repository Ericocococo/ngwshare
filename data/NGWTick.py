import requests
import json
import time
import traceback

from ngwshare.utils.date_util import str2datetime
from ngwshare.utils.http_util import get_ua
import pandas as pd
import datetime



def get_stock_tick(code=None,start=None,end=None,limit=1000):
    split_list = code.split('.')
    symbol = split_list[0]
    exchange = 'SHSE' if split_list[1] == 'SH' else 'SZSE'
    # url = 'https://testshq.niuguwang.com/aquote/quote/Tick.ashx?startTime={}&endTime={}&symbol={}&exchange={}&limit={}'\
    #     .format(start,end,symbol,exchange,limit)
    url = 'https://shq.niuguwang.com/aquote/quote/Tick.ashx?startTime={}&endTime={}&symbol={}&exchange={}&limit={}'\
        .format(start,end,symbol,exchange,limit)
    try:
        headers = {'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        if response_json['error_no'] == 0:
            return pd.DataFrame(response_json['data'])
        else:
            return pd.DataFrame()
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    import time
    t1 = time.time()

    # 获取股票tick数据 limit限制条数
    data = get_stock_tick(code='000001.SZ',start='2021-07-15 09:30:00',end='2021-07-15 15:00:00',limit=5000)
    print(data)

    print(time.time()-t1)


