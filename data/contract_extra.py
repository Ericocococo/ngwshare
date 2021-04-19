from ngwshare.utils.date_util import str2datetime
__author__ = 'wangjian'
from ngwshare.utils.http_util import get_ua
import requests
import traceback
import json
import pandas as pd
import datetime


# 根据日期返回交易日期
def ReturnTradingDate(DatetimeStr=None):
    dt_date = str(str2datetime(DatetimeStr))[:19]
    str_date = dt_date.replace('-', '').replace(':', '').replace(' ', '')
    try:
        url = "https://apigateway.inquantstudio.com/api/BasicData/GetTradeDate?time={}".format(str_date)
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('error_no') == 0:
                return str(str2datetime(response_json.get('data')))[:10]
            else:
                return None
        except:
            return None



# 返回历史主力合约
def get_HisMainContract(variety=None,start=None,end=None):
    start_ = str(str2datetime(start))[:19].replace('-', '').replace(':', '').replace(' ', '')
    end_ = str(str2datetime(end))[:19].replace('-', '').replace(':', '').replace(' ', '')
    body = {'varietyCode': variety,'begin': int(start_),'end': int(end_)}
    # print(json.dumps(body))
    try:
        url = "https://apigateway.inquantstudio.com/api/BasicData/GetHisMain"
        # url = "https://dev-apigateway.inquantstudio.com/api/BasicData/GetHisMain"
        headers = {'User-Agent': get_ua(),
                   "Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(body),headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('error_no') == 0:
                return pd.DataFrame(response_json.get('data'))
            else:
                return response_json.get('error_info')
        except:
            print(traceback.format_exc())



# 根据合约类别获取交易时间
def get_TradeDatetime(variety=None,start=None,end=None):
    start_ = str(str2datetime(start))[:19].replace('-', '').replace(':', '').replace(' ', '')
    end_ = str(str2datetime(end)+datetime.timedelta(days=1))[:19].replace('-', '').replace(':', '').replace(' ', '')
    body = {'varietyCode': variety,'begin': int(start_),'end': int(end_)}
    # print(json.dumps(body))
    try:
        url = "https://apigateway.inquantstudio.com/api/BasicData/GetOpenTimesByCode"
        # url = "https://dev-apigateway.inquantstudio.com/api/BasicData/GetOpenTimesByCode"
        headers = {'User-Agent': get_ua(),
                   "Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(body),headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('error_no') == 0:
                # return pd.DataFrame(response_json.get('data'))
                return response_json.get('data')
            else:
                return response_json.get('error_info')
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    import time
    import ngwshare as ng

    # trading_date = ReturnTradingDate(DatetimeStr='2021-03-26 01:09:00')
    # print(trading_date)

    # data = ng.get_HisMainContract(variety='v', start='2021-04-08', end='2021-04-09')
    # print(data)





    # a = ReturnTradingDate(DatetimeStr='20210410020000')
    # print(a)



    data = ng.get_TradeDatetime(variety='MA', start='2021-04-08', end='2021-05-13')
    print(data)

    # a = str(datetime.datetime.now())[:19]
    # b = str(datetime.datetime.now())[:19].replace('-','').replace(' ','').replace(':','')
    # print(a)
    # print(b)

    t11 = time.time()

    for b_e in data:
        begin = b_e.get('begin')
        end = b_e.get('end')
        # datetimeStr = '20210406101500'
        datetimeStr = str(datetime.datetime.now())[:19].replace('-', '').replace(' ', '').replace(':', '')
        if datetimeStr >= begin and datetimeStr < end:
            print('1111111111111')

        print(begin,end)

    print(time.time()-t11)



    # print(data.loc[1].begin)
    # print(type(data.loc[1].begin))





















