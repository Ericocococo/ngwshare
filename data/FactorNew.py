import requests
import pandas as pd
import json
import urllib3
from ngwshare.utils.http_util import get_ua

def getRiskFactor(body=None):
    pd.set_option('precision', 34)
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getriskdata"
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getriskdata'
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df




def getStyleFactor(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getstyledata'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getstyledata"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df




def getCSResidual(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getresidualedata'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getresidualedata"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df





def getSpecificRisk(body=None):
    # url = 'http://127.0.0.1:5000/factor/getnonfactordata'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getnonfactordata"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df




def getAlphaFactor(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getalphadata'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getalphadata"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df



def getCSFactorReturns(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getcsfactor'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getcsfactor"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    df = pd.DataFrame(dict, columns=json.loads(text)["col_name"])
    return df




def getCovMatrix(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getcovmatrix'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getcovmatrix"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    df = pd.DataFrame(dict, columns=json.loads(text)["col_name"])
    return df




def getCovMatrixCol(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getcovmatrixcol'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getcovmatrixcol"
    # url = "http://dev-www.test.niuguwang/NorthJg/GetNorthJg/hsweight"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    df = pd.DataFrame(dict, columns=json.loads(text)["col_name"])
    return df


if __name__ == '__main__':
    import ngwshare as ng

    body = {
        'stock_list': ['002509.SZ'],
        'start': '2016-08-10',
        'end': ' 2016-08-10',
        'field_list': ['IndustrySW_vsZZ500inZZ500']
    }
    data = ng.getRiskFactor(body=body)
    print(data)
    # print("getRiskFactor:", data)



    body = {
        'stock_list': ['600276.SH', '002081.SZ', '600176.SH'],
        'start': '2015-01-05',
        'end': '2015-01-05',
        'field_list': ['Industry_vsHS300inHS300', "Size_vsHS300inHS300"]
    }
    data = ng.getStyleFactor(body=body)
    print(data)
    # print("getStyleFactor", data)


    body = {
        'stock_list': ['000725.SZ','000793.SZ', '000839.SZ'],
        'start': '2015-01-06',
        'end': '2015-01-06',
        'field_list': ['value']
    }
    data = ng.getCSResidual(body=body)
    print(data)
    # print("getCSResidual", data)


    body = {
        'stock_list': ['000157.SZ','000425.SZ', '000559.SZ'],
        'start': '2016-01-13',
        'end': '2016-01-13',
        'field_list': ['value']
    }
    data = ng.getSpecificRisk(body=body)
    print(data)
    # print("getSpecificRisk", data)


    body = {
        'stock_list': ['000027.SZ','000402.SZ', '000559.SZ'],
        'start': '2015-01-05',
        'end': '2015-01-06',
        'field_list': ['Liquidity_HS300', 'alpha3_HS300']
    }
    data = ng.getAlphaFactor(body=body)
    print(data)
    # print("getAlphaFactor", data)



    body = {
        'start': '2015-01-06',
        'end': '2015-01-07',
        'field_list': ['ZZ500_1']
    }
    data = ng.getCSFactorReturns(body=body)
    print(data)
    # print("getCSFactorReturns", data)



    body = {
        'start': '2016-01-13',
        'end': '2016-01-14',
        'field_list': ['ZZ500_1']
    }
    data = ng.getCovMatrix(body=body)
    print(data)
    # print("getCovMatrix", data)


    body = {
        'start': '2016-01-13',
        'end': '2016-01-14',
        'field_list': ['HS300_1']
    }
    data = ng.getCovMatrixCol(body=body)
    print(data)
    # print("getCovMatrixCol", data)




