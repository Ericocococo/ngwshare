import json
import traceback
import pandas as pd
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)
import requests

__author__ = 'wangjian'


# host = '127.0.0.1:5001'
host = '192.168.3.212:8080'

def conn_FromDate(body=None):
    try:
        headers = {"Content-Type": "application/json"}
        url = "http://{}/api/fromDate".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        # print(response_json)
        if response_json["resultCode"] == 0:
            if response_json.get('data'):
                df_data = pd.DataFrame(response_json['data'])
                columns_list = []
                field_list = body.get('field_list')
                if field_list:
                    columns_list.extend(field_list)
                df_data.columns = columns_list
                return df_data
            else:
                return 'no data exist.'
        else:
            return 'select error.'
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    from pprint import pprint



    # table = 'LC_SHSCTradeStat'
    # field_list = ["EndDate", "TradingType", "BTradeValue", "STradeValue_DA", "STradeValueChange"]

    # table = 'LC_ZHSCTradeStat'
    # field_list = ["EndDate", "Currency", "IfAdjusted", "STradeValue_DA", "BTradeValueChange_DA","STradeValueChange_DA"]

    table = 'QT_SHSZHSCTradingDay'
    field_list = ["EndDate", "TradingType", "IfWeekEnd", "IfYearEnd", "UpdateTime","InfoSource"]

    body = {
        "table": table,
        "field_list": field_list,
        "alterField": "EndDate",
        "startDate": "2020-01-01",
        "endDate": "2020-05-26"
    }

    # data = conn_FromCode(body)
    data = conn_FromDate(body)

    pprint(data)

    