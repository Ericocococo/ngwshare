import requests
import json
import time
import traceback
from ngwshare.utils.date_util import str2datetime
from ngwshare.utils.http_util import get_ua
import pandas as pd
import datetime

def get_allStock():
    try:
        headers = {'User-Agent': get_ua()}
        url = "https://stq.niuguwang.com/jy/innercode"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            df_data.columns = ['innercode', 'code', 'name', 'market', 'boardname', 'stocktype', 'insert_time',
                               'update_time']
            return df_data
        else:
            return None

def getRZRQStock(start=None,end=None,stock_list=None):
    if stock_list:
        all_df = get_allStock()
        innercode_list = all_df[all_df['code'].isin(stock_list)]['innercode'].tolist()
    else:
        innercode_list = []
    body = {
        'start':start,
        'end': end,
        'innercode_list': innercode_list,
    }
    url = 'https://stq.niuguwang.com/jydata/rzrqstock'
    try:
        headers = {"Content-Type": "application/json",'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        # print(response_json)
        if response_json['resultCode'] == 0:
            return pd.DataFrame(response_json['data'])
        else:
            return response_json['data']
    except Exception:
        print(traceback.format_exc())



if __name__ == '__main__':
    import ngwshare as ng
    # 获取个股融资融券
    data = ng.getRZRQStock(start='2021-06-14',end='2021-06-15',stock_list=['000001.SZ','600016.SH','300383.SZ'])
    print(data)

