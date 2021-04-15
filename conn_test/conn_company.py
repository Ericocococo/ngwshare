import json
import traceback
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import requests

__author__ = 'wangjian'


# host = '127.0.0.1:5001'
host = '192.168.3.212:8080'

def conn_FromCompany(body=None):
    try:
        headers = {"Content-Type": "application/json"}
        url = "http://{}/api/fromCompany".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        print(response_json)
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
    code_list = ["000858.SZ", "600722.SH", "000895.SZ", "600006.SH"]

    # field_list = ["EndDate"]

    # table = 'LC_NewestFinaIndex'
    # field_list = ["ShareCapitalBeforeAdjust", "SHareCapitalIncr", "RetainedProfitAfterAdjust", "NAPS", "EPS"]

    # table = 'LC_DerivativeData'
    # field_list = ["OperatingCostTTM", "TotalOperatingRevenueTTM", "AdministrationExpenseTTM", "NIFromOperatingTTM", "FCFF"]

    # table = 'LC_MainDataNew'
    # field_list = ["BasicEPS", "EPS","ROE", "ROECut", "WROECut", "ProfitatISA"]

    # table = 'LC_MainQuarterData'
    # field_list = ["EndDate", "BasicEPS", "OperatingReenue", "CashEquialents", "TotalShares"]

    table = 'LC_MainDataNew'
    field_list = ["EndDate","InfoPublDate","EPS","ROE"]

    # table = 'LC_IPODeclaration'
    # field_list = ["InfoPublDate", "CSRCIndustryName"]

    body = {
        "table": table,
        "code_list": code_list,
        # "all_code": True,
        "field_list": field_list,
        "alterField": "InfoPublDate",
        "startDate": "2020-01-01",
        "endDate": "2020-08-12"
    }

    data = conn_FromCompany(body)

    print(data)

# # 每股收益 eps
# # 市盈率 pe
# # 外资昨日买入 foreign_money_in_buy_yesterday (fmiby)
# # 净资产收益率 roe
# # 净利增长率 net_tate (nt)
#
# # 行业板块 plate_boardname
# data_temp['eps'] = 0
# data_temp['pe'] = 0
# data_temp['fmiby'] = 0
# data_temp['roe'] = 0
# data_temp['nt'] = 0
# data_temp['plate_boardname'] = '半导体'