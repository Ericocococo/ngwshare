import requests
import json
import time
import traceback

from ngwshare.utils.date_util import str2datetime
from ngwshare.utils.http_util import get_ua
import pandas as pd
import datetime

def getFactor(body=None):
    url = 'http://stq.niuguwang.com/factor/getfactor'
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        # print(response_json)
        if response_json['resultCode'] == 0:
            return pd.DataFrame(response_json['data'])
        else:
            return pd.DataFrame()
    except Exception:
        print(traceback.format_exc())

def upsertFactor(body=None):
    url = 'http://stq.niuguwang.com/factor/addfactor'
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        # print(response_json)
        if response_json['resultCode'] == 0:
            return response_json['data']
        else:
            return response_json['data']
    except Exception:
        print(traceback.format_exc())

if __name__ == '__main__':
    t11 = time.time()
    import ngshare as ng

    body = {
        'stock_list': ['000002.SZ','000008.SZ'],
        'start': '2021-01-05',
        'end': '2021-04-06',
        'field_list': ['alpha3', 'alpha13', 'alpha26', 'cash2price', 'SEWithoutMIToTL']
    }
    data = ng.getFactor(body=body)
    print(data)

    # start_ts = int(str2datetime('2021-04-05').timestamp())
    # end_ts = int(str2datetime('2021-04-06').timestamp())
    # print(start_ts)
    # print(end_ts)



    # body = {'data':[
    #     {
    #         'StockCode': '000002.SZ',
    #         'Name': '万  科',
    #         'InnerCode': 2318,
    #         'Date': '2021-04-05',
    #         'factor9':111111
    #     }
    # ]}
    # data = upsertFactor(body=body)
    # print(data)


    # body = {
    #     'stock_list': ['000002.SZ','000008.SZ'],
    #     'start': '2021-04-05',
    #     'end': '2021-04-06',
    #     'field_list': ['factor10', 'factor12', 'factor9']
    # }
    # data = getFactor(body=body)
    # print(data)
    #
    # a = data.loc[0]['factor9']
    # print(a)
    # print(type(a))
    #
    # a = data.loc[2]['factor9']
    # print(a)
    # print(type(a))



    print(time.time()-t11)



