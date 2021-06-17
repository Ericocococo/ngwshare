__author__ = 'wangjian'
from ngwshare.utils.http_util import get_ua
import requests
import traceback
import json
import pandas as pd


def get_hxl2():
    try:
        url = "https://stq.niuguwang.com/zljl/hxl2"
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
                return pd.DataFrame(response_json.get('data'))
            else:
                return pd.DataFrame()
        except:
            return pd.DataFrame()

if __name__ == '__main__':
    data = get_hxl2()
    print(data)

