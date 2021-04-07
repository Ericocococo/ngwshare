__author__ = 'wangjian'
from ngwshare.utils.http_util import get_ua
import requests
import traceback
import json
import pandas as pd


def get_USKline(symbol=None,klineType=None,end=None,count=None):
    try:
        if end:
            url = "http://testcaklineus.huanyingzq.com/USKline/Kline?symbol={}&klineType={}&end={}&count={}".format(symbol,klineType,end,count)
        else:
            url = "http://testcaklineus.huanyingzq.com/USKline/Kline?symbol={}&klineType={}&count={}".format(symbol,klineType,count)
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('code') == 0:
                return pd.DataFrame(response_json.get('data'))
            else:
                return None
        except:
            return None






















