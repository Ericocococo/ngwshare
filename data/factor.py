import requests
import json
import time
import traceback

from ngwshare.utils.date_util import str2datetime
from ngwshare.utils.http_util import get_ua
import pandas as pd
import datetime

def getFactor(body=None):
    url = 'https://stq.niuguwang.com/factor/getfactor'
    try:
        headers = {"Content-Type": "application/json","Ngw-Token":"Ngw123456",'User-Agent':get_ua()}
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
    url = 'https://stq.niuguwang.com/factor/addfactor'
    try:
        headers = {"Content-Type": "application/json","Ngw-Token":"Ngw123456",'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        # print(response_json)
        if response_json['resultCode'] == 0:
            return response_json['data']
        else:
            return response_json['data']
    except Exception:
        print(traceback.format_exc())

def getFactorColumns():
    url = 'https://stq.niuguwang.com/factor/GetFactorColumns'
    try:
        headers = {"Content-Type": "application/json","Ngw-Token":"Ngw123456",'User-Agent':get_ua()}
        response = requests.get(url,headers=headers).content.decode()
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
    import ngwshare as ng

    body = {
        'stock_list': ["000001.SZ"],
        'start': "2016-12-30",
        'end': "2021-04-15",
        'field_list': ng.getFactorColumns(),
    }
    AlphaDFi = ng.getFactor(body=body)
    print(AlphaDFi)


    # body = {
    #     'stock_list': ['000002.SZ','000008.SZ'],
    #     'start': '2021-01-05',
    #     'end': '2021-04-14',
    #     'field_list': ['alpha3', 'alpha13', 'Liquidity', 'ROE', 'NB_ratio']
    # }
    # data = ng.getFactor(body=body)
    # print(data)
    #
    #
    # columns = ng.getFactorColumns()
    # print(columns)
    # print(len(columns))

    # a = [
    #                  "alpha3",
    #                  "alpha13",
    #                  "alpha26",
    #                  "alpha44",
    #                  "alpha50",
    #                  "HCHL",
    #                  "HC",
    #                  "MomAdj",
    #                  "LC",
    #                  "Liquidity",
    #                  "PB",
    #                  "ROA",
    #                  "ROE",
    #                  "OpRGrowth",
    #                  "cash2price",
    #                  "DA_ratio",
    #                  "WC2TA",
    #                  "GP2TA",
    #                  "EBITDA2TL",
    #                  "NBtracking",
    #                  "EfChg_b60v5",
    #                  "hurst60",
    #                  "alpha012",
    #                  "alpha040",
    #                  "vroc5",
    #                  "rvi10",
    #                  "arc2",
    #                  "w_r5",
    #                  "acd20",
    #                  "SuperQuickRatio",
    #                  "FixedAssetTRate",
    #                  "AdminiExpenseRate",
    #                  "SEWithoutMIToTL",
    #                  "TOperatingCostToTOR",
    #                  "SEWMIToInterestBearDebt",
    #                  "NetOperateCashFlowYOY",
    #                  "SEWithoutMIGrowRateYTD",
    #                  "TORGrowRate",
    #                  "FCFE",
    #                  "OperatingRevenueYOY",
    #                  "closeReturn_Last",
    #                  "Earnings_QG",
    #                  "NB_shr",
    #                  "NB_ratio",
    #     ]
    # print(len(a))
    # #
    # for i in a:
    #     if i not in columns:
    #         print(i)
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



