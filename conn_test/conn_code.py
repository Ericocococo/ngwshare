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

def conn_FromCode(body=None):
    try:
        headers = {"Content-Type": "application/json"}
        url = "http://{}/api/fromCode".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        # print(response_json)
        if response_json["resultCode"] == 0:
            if response_json.get('data'):
                df_data = pd.DataFrame(response_json['data'])
                columns_list = []
                field_list = body.get('field_list')
                if field_list:
                    columns_list = ['code', 'name']
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

    # code_list = ["600006.SH"]
    # code_list = ["000858.SZ","600722.SH","000895.SZ","600006.SH"]
    code_list = ["000858.SZ"]


    # table = 'QT_DailyQuote'
    # field_list = ["TradingDay", "PrevClosePrice", "OpenPrice", "HighPrice", "LowPrice"]

    # table = 'QT_Performance'
    # field_list = ["TradingDay", "PrevClosePrice", "TurnoverVolume", "RangePCT", "ChangePCTRW"]

    # table = 'QT_PerformanceData'
    # field_list = ["MaxRisingUpDays", "AHPremiumRate50", "TradingDay", "HighestPrice", "HighestPriceTW"]

    table = 'LC_DIndicesForValuation'
    field_list = ["TradingDay", "PB", "PCFTTM", "PCFS", "PS", "PE"]

    # table = 'LC_SHSZHSCHoldings'
    # field_list = ["SHSZHSCode", "SecuAbbr", "SharesHolding", "Holdratio", "InsertTime"]

    body = {
        "table": table,
        "code_list": code_list,
        # "all_code": True,
        "field_list": field_list,
        "alterField": "TradingDay",
        # "alterField": "EndDate",
        "startDate": "2020-08-10",
        "endDate": "2020-08-12"
    }

    data = conn_FromCode(body)
    print(data)
    pe_data = data['PE'].tolist()[-1]
    print(pe_data)





