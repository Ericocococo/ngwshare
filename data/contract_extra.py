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



if __name__ == '__main__':
    trading_date = ReturnTradingDate(DatetimeStr='2021-03-27 18:09:00')
    print(trading_date)








