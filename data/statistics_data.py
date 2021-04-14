__author__ = 'wangjian'
from ngwshare.utils.http_util import get_ua
import requests
import traceback
import json
import pandas as pd
import time



def get_SearchData(start=None,end=None):
    start = start.replace('-', '').replace(':', '').replace(' ', '')
    end = end.replace('-', '').replace(':', '').replace(' ', '')
    try:
        url = "https://stq.niuguwang.com/zljl/search?start={}&end={}".format(start,end)
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
                df_data = pd.DataFrame(response_json.get('data'))
                return df_data
            else:
                return None
        except:
            return None



def get_SelectSelfMaxMin():
    try:
        url = "https://stq.niuguwang.com/zljl/MaxMin"
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
                return None
        except:
            return None




def get_SelectSelf(start=None,end=None):
    try:
        url = "https://stq.niuguwang.com/zljl/zixuan?start={}&end={}".format(start,end)
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
                df_data = pd.DataFrame(response_json.get('data'))
                return df_data
            else:
                return None
        except:
            return None


if __name__ == '__main__':
    t11 = time.time()
    import ngwshare as ng


    data = ng.get_SearchData(start='2021-03-23 00:00:00',end='2021-03-23 23:59:59')
    print(data)

    data = ng.get_SelectSelfMaxMin()
    print(data)

    data = ng.get_SelectSelf(start=1, end=200)
    print(data)


    print(data.loc[0]['Codes'])

    print(time.time()-t11)











