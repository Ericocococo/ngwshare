from ngwshare.utils.date_util import str2datetime
__author__ = 'wangjian'
from ngwshare.utils.http_util import get_ua
import requests
import traceback
import json
import pandas as pd



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


if __name__ == '__main__':
    import ngshare as ng

    # trading_date = ReturnTradingDate(DatetimeStr='2021-03-27 18:09:00')
    # print(trading_date)

    data = ng.get_HisMainContract(variety='v', start='2021-04-08', end='2021-04-09')
    print(data)







