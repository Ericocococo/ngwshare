import time
import json
import traceback
import requests
import datetime
import pandas as pd
import numpy as np
from ngwshare.conn_db.conn_sqlserver import conn_sqlserver_select
from ngwshare.conn_db.conn_mysql import conn_mysql_select
from ngwshare.utils.date_util import str2datetime, get_date_length, is_trading_day
# from ngwshare.utils.log_util import logger
from ngwshare.utils.http_util import get_ua
from ngwshare.constants import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
    MYSQL_USER,
    MYSQL_PASSWORD,
    HOST,
    PRE
)
from ngwshare.constants import (
    SQL_SERVER_HOST,
    SQL_SERVER_DATABASE,
    SQL_SERVER_USER,
    SQL_SERVER_PASSWORD
)


pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

host = HOST
pre = PRE
requests.DEFAULT_RETRIES = 10

def get_k_data(code=None, freq=None, start=None, end=None, bars=None):
    if bars:
        len = 200 if bars<100 else 500
        start =str(str2datetime(end)-datetime.timedelta(days=bars+len))
        # print(start,end)
    try:
        url = "https://{}/jy/dailyQuote?secuCodeMarket={}&startDate={}&endDate={}" \
            .format(host, code, start, end)
        # print(url)
        response = requests.get(url)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close', 'preclose', 'volume', 'value']
            # df_data_ = df_data[['date', 'open', 'high', 'low', 'close', 'preclose','volume','value']]
            data_ = df_data.sort_values(by='date').reset_index(drop=True)
            if bars:
                return data_[-bars:].reset_index(drop=True)
            else:
                return data_
        else:
            return None


def get_stock_basic(code=None):
    try:
        url = "https://{}/jy/stockBasic?secuCodeMarket={}".format(host,code)
        response = requests.get(url)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            return response_json['data']
        else:
            return None


def get_all_stock():
    try: # http://192.168.8.104:3389/api/stockAll
        url = "https://{}/jy/stockAll".format(host)
        # print(url)
        response = requests.get(url)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            df_data.columns = ['code', 'name']
            return df_data
        else:
            return None


def get_performance(date):
    try:
        url = "https://{}/jy/performance?date={}".format(host,date)
        response = requests.get(url)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            df_data.columns = ['code', 'name', 'date', 'total_MV', 'negotiable_MV', 'pre_close',
                               'open', 'high', 'low', 'close', 'trunover_volume', 'turnover_value']
            return df_data
        else:
            return None


def get_dIndicesForValuation(date):
    try:
        url = "https://{}/jy/dIndicesForValuation?date={}".format(host,date)
        response = requests.get(url)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            df_data.columns = ['code', 'name', 'date', 'PELYR', 'PE', 'PB', 'PCF', 'PS', 'InsertTime']
            return df_data
        else:
            return None


def get_c_RR_ResearchReport(name=None,start=None,end=None):
    try:
        url = "https://{}/jy/c_RR_ResearchReport?name={}&startDate={}&endDate={}"\
            .format(host,name,start,end)
        response = requests.get(url)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            return df_data
        else:
            return None


def get_specialTrade():
    try:
        url = "https://{}/jy/specialTrade".format(host)
        response = requests.get(url)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            df_data.columns = ['code', 'name', 'date', 'type']
            return df_data
        else:
            return None



def get_financialData(table,stock,filed_list,start,end):
    if len(stock)>1:
        stock = tuple(stock)
    else:
        stock = str(tuple(stock)).replace(',','')
    try:
        url = "https://{}/jy/financialData?table={}&code={}&field={}&startDate={}&endDate={}"\
            .format(host,table,stock,filed_list,start,end)
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        response = requests.get(url,headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            return df_data
        else:
            return None



def get_financialDataPro(table,alterFiled,filed_list,start,end):
    try:
        url = "https://{}/jy/newestFinaIndex?table={}&alterField={}&field={}&startDate={}&endDate={}"\
            .format(host,table,alterFiled,filed_list,start,end)
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        response = requests.get(url,headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            return df_data
        else:
            return None


def get_fromCode(body=None):
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        url = "https://{}/jy/fromCode".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(response_json)
        if response_json.get("resultCode") == 0:
            if response_json.get('data'):
                df_data = pd.DataFrame(response_json['data'])
                columns_list = []
                field_list = body.get('field_list')
                if field_list:
                    columns_list = ['code', 'name']
                    columns_list.extend(field_list)
                df_data.columns = columns_list
                # 区分sz,sh
                if 'code_list' in body.keys():
                    df_data = df_data[df_data.code.isin(body['code_list'])]
                return df_data
            else:
                return 'no data exist.'
        else:
            return 'select error.'




def get_fromCompany(body=None):
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        url = "https://{}/jy/fromCompany".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(response_json)
        if response_json.get("resultCode") == 0:
            if response_json.get('data'):
                df_data = pd.DataFrame(response_json['data'])
                columns_list = []
                field_list = body.get('field_list')
                if field_list:
                    columns_list = ['code', 'name']
                    columns_list.extend(field_list)
                df_data.columns = columns_list
                if 'code_list' in body.keys():
                    df_data = df_data[df_data.code.isin(body['code_list'])]
                return df_data
            else:
                return 'no data exist.'
        else:
            return 'select error.'



def get_fromDate(body=None):
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        url = "https://{}/jy/fromDate".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
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


def get_fromDateName(body=None):
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        url = "https://{}/jy/fromDateName".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
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


def get_fromTable(body=None):
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        url = "https://{}/jy/fromTable".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
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



def get_fromName(body=None):
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        url = "https://{}/jy/fromName".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
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


# -------------------------------------------------------------------------------------

def get_type_from_freq(freq):
    if freq == '5m':
        return 1
    if freq == '15m':
        return 2
    if freq == '30m':
        return 3
    if freq == '60m':
        return 4
    if freq == 'd':
        return 5
    if freq == 'w':
        return 6
    if freq == 'mon':
        return 9
    if freq == '1m':
        return 11


def get_ex_from_adj(adj):
    if adj is None:
        return 0
    if adj == 'qfq':
        return 1
    if adj == 'hfq':
        return 2


def fixing_k_data(data, code, start, end):
    df_data = pd.DataFrame(data)
    df_data = df_data[['times', 'highp', 'openp', 'lowp', 'nowv', 'preclose', 'curvol', 'curvalue']]
    trading_day = [str(datetime.datetime.strptime(str(i), '%Y%m%d%H%M%S')) for i in df_data['times']]
    high = [round(float(i) / 100, 4) for i in df_data['highp']]
    open = [round(float(i) / 100, 4) for i in df_data['openp']]
    low = [round(float(i) / 100, 4) for i in df_data['lowp']]
    close = [round(float(i) / 100, 4) for i in df_data['nowv']]
    preclose = [round(float(i) / 100, 4) for i in df_data['preclose']]
    vol = [round(float(i), 4) for i in df_data['curvol']]

    data_dict = {}
    data_dict['code'] = [code for _ in range(len(trading_day))]
    data_dict['date'] = trading_day
    data_dict['open'] = open
    data_dict['high'] = high
    data_dict['low'] = low
    data_dict['close'] = close
    data_dict['preclose'] = preclose
    data_dict['volume'] = vol
    data_dict['value'] = df_data['curvalue']
    df_data_ = pd.DataFrame(data_dict)
    if len(start) == 10:
        start += ' 00:00:00'
    if len(end) == 10:
        end += ' 00:00:00'
    df_data_n = df_data_.loc[(df_data_["date"] >= start) & (df_data_["date"] <= end)]
    return df_data_n.sort_values(by='date').reset_index(drop=True)


def fixing_k_data_m(data, code):
    df_data = pd.DataFrame(data)
    df_data = df_data[['times', 'highp', 'openp', 'lowp', 'nowv', 'preclose', 'curvol', 'curvalue']]
    trading_day = [str(datetime.datetime.strptime(str(i), '%Y%m%d%H%M%S')) for i in df_data['times']]
    high = [round(float(i) / 100, 4) for i in df_data['highp']]
    open = [round(float(i) / 100, 4) for i in df_data['openp']]
    low = [round(float(i) / 100, 4) for i in df_data['lowp']]
    close = [round(float(i) / 100, 4) for i in df_data['nowv']]
    preclose = [round(float(i) / 100, 4) for i in df_data['preclose']]
    vol = [round(float(i), 4) for i in df_data['curvol']]

    data_dict = {}
    data_dict['code'] = [code for _ in range(len(trading_day))]
    data_dict['date'] = trading_day
    data_dict['open'] = open
    data_dict['high'] = high
    data_dict['low'] = low
    data_dict['close'] = close
    data_dict['preclose'] = preclose
    data_dict['volume'] = vol
    data_dict['value'] = df_data['curvalue']
    df_data_ = pd.DataFrame(data_dict)
    return df_data_.sort_values(by='date').reset_index(drop=True)


def get_stock_data_raw(code=None, freq=None, adj=None, start=None, end=None, bars=None):
    """
    :param code: 证券代码
    :param freq: 频率  1m  5m  15m  30m  60m  d   w   month
    :param adj: 复权类型  None：不复权（除权）   qfq：前复权    hfq：后复权
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    # inner_code_dict
    if bars:
        len = 200 if bars<100 else 500
        start =str(str2datetime(end)-datetime.timedelta(days=bars+len))

    df_ = get_allStock()
    try:
        innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
    except:
        return pd.DataFrame()
    # print(innerCode)
    if innerCode is None:
        return pd.DataFrame()

    count = get_date_length(start, end)  # 开始日期到目前截至日期的len
    # print(start,end)
    end_ = str(str2datetime(end) + datetime.timedelta(days=1))
    start_ = end_.replace('-', '').replace(':', '').replace(' ', '')

    type = get_type_from_freq(freq)
    ex = get_ex_from_adj(adj)

    # url = ''
    if ex:
        url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&start={}&count={}&ex={}" \
            .format(pre, innerCode, type, start_, count, ex)
    else:
        url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&start={}&count={}" \
            .format(pre, innerCode, type, start_, count)
    # print(url)
    try:
        # t = time.time()
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(response_json)
        # print(time.time()-t)
        if response_json:
            data = response_json['timedata']
            if data:
                # for i in data:
                #     print(i)
                df_data = fixing_k_data(data, code, start, end)
                # print(df_data)
                if bars:
                    return df_data[-bars:].reset_index(drop=True)
                else:
                    return df_data
            else:
                # print('休市.')
                return pd.DataFrame()
        else:
            return pd.DataFrame()


def get_stock_data_raw_m(code=None, freq=None, adj=None, start=None, end=None, bars=None):
    """
    :param code: 证券代码
    :param freq: 频率  1m  5m  15m  30m  60m  d   w   month
    :param adj: 复权类型  None：不复权（除权）   qfq：前复权    hfq：后复权
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    # inner_code_dict
    df_ = get_allStock()
    try:
        innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
    except:
        return pd.DataFrame()
    # print(innerCode)
    if innerCode is None:
        return pd.DataFrame()

    type = get_type_from_freq(freq)
    ex = get_ex_from_adj(adj)
    url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}&ex={}" \
        .format(pre, innerCode, type, bars, ex)

    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            data = response_json['timedata']
            if data:
                df_data = fixing_k_data_m(data, code)
                return df_data
            else:
                return pd.DataFrame()
        else:
            return pd.DataFrame()


def get_stock_data(code=None, freq=None, adj=None, start=None, end=None, bars=None):
    delay_times = 5
    i = 0
    while i<delay_times:
        # print(i,delay_times)
        data = pd.DataFrame()
        if (end and bars) or (start and end):
            data = get_stock_data_raw(code=code, freq=freq, adj=adj, start=start, end=end, bars=bars)
        elif end is None and bars:
            data = get_stock_data_raw_m(code=code, freq=freq, adj=adj, start=start, end=end, bars=bars)
        else:
            return pd.DataFrame()

        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data

        i+=1
        time.sleep(0.01)
        continue
    return pd.DataFrame()

# -------------------------------------------------------------------------------------------
def get_stock_data_inner_raw(innercode=None, freq=None, adj=None, bars=None):
    """
    :param code: 证券代码
    :param freq: 频率  1m  5m  15m  30m  60m  d   w   month
    :param adj: 复权类型  None：不复权（除权）   qfq：前复权    hfq：后复权
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    type = get_type_from_freq(freq)
    ex = get_ex_from_adj(adj)
    url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}&ex={}" \
        .format(pre, innercode, type, bars, ex)

    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            data = response_json['timedata']
            df_data = pd.DataFrame(data)
            return df_data
        else:
            return pd.DataFrame()


def get_stock_data_inner_rr(code=None, innercode=None, freq=None, adj=None, bars=None):
    """
    :param code: 证券代码
    :param freq: 频率  1m  5m  15m  30m  60m  d   w   month
    :param adj: 复权类型  None：不复权（除权）   qfq：前复权    hfq：后复权
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    type = get_type_from_freq(freq)
    ex = get_ex_from_adj(adj)
    url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}&ex={}" \
        .format(pre, innercode, type, bars, ex)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            data = response_json['timedata']
            if data:
                df_data = fixing_k_data_m(data, code)
                return df_data
            else:
                return pd.DataFrame()
        else:
            return pd.DataFrame()


def get_stock_data_inner(code=None, innercode=None, freq=None, adj=None, bars=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_stock_data_inner_rr(code=code, innercode=innercode, freq=freq, adj=adj, bars=bars)
        if not data.empty:
            return data

        i += 1
        time.sleep(0.01)
        continue
    return pd.DataFrame()

# ------------------------------------------------------------------------------------------------------
def get_plate_data_inner_rr(code=None, innercode=None, freq=None, adj=None, bars=None):
    """
    :param code: 证券代码
    :param freq: 频率  1m  5m  15m  30m  60m  d   w   month
    :param adj: 复权类型  None：不复权（除权）   qfq：前复权    hfq：后复权
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    type = get_type_from_freq(freq)
    ex = get_ex_from_adj(adj)
    url = "{}hq.niuguwang.com/aquote/plate/kline.ashx?code={}&type={}&count={}&ex={}" \
        .format(pre, innercode, type, bars, ex)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(response_json)
        if response_json:
            data = response_json['timedata']
            if data:
                df_data = fixing_k_data_m(data, code)
                return df_data
            else:
                return pd.DataFrame()
        else:
            return pd.DataFrame()


def get_plate_data_inner_raw(innercode=None, freq=None, adj=None, bars=None):
    """
    :param code: 证券代码
    :param freq: 频率  1m  5m  15m  30m  60m  d   w   month
    :param adj: 复权类型  None：不复权（除权）   qfq：前复权    hfq：后复权
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    type = get_type_from_freq(freq)
    ex = get_ex_from_adj(adj)
    url = "{}hq.niuguwang.com/aquote/plate/kline.ashx?code={}&type={}&count={}&ex={}" \
        .format(pre, innercode, type, bars, ex)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            data = response_json['timedata']
            df_data = pd.DataFrame(data)
            return df_data
        else:
            return pd.DataFrame()


def get_plate_data_inner(code=None, innercode=None, freq=None, adj=None, bars=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_plate_data_inner_rr(code=code, innercode=innercode, freq=freq, adj=adj, bars=bars)
        if not data.empty:
            return data

        i += 1
        time.sleep(0.01)
        continue
    return pd.DataFrame()

# -------------------------------------------------------------------------------------------
# 获取深度信息
def get_depth_raw(code=None):
    try:
        innerCode = int(code2nameInner(code.split('.')[0])[2])
        # df_ = get_allStock()
        # innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
    except:
        return None
    if innerCode is None:
        return None
    url = "{}hq.niuguwang.com/aquote/quotedata/detailfivedish.ashx?code={}".format(pre,innerCode)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(time.time()-t)
        if response_json:
            return fixing_depth(response_json,code)
        else:
            return None


def get_depth(code=None):
    delay_times = 5
    i = 0
    while i<delay_times:
        data = get_depth_raw(code=code)
        if data:
            return data
        
        i+=1
        time.sleep(0.01)
        continue


def fixing_depth(data,code):
    depth = {}
    depth['time'] = str(datetime.datetime.strptime(str(data['time']), '%Y%m%d%H%M%S'))
    depth['code'] = code
    depth['asks']=[
        [abs(float(data['ask1p'])),int(data['ask1v'])],
        [abs(float(data['ask2p'])),int(data['ask2v'])],
        [abs(float(data['ask3p'])),int(data['ask3v'])],
        [abs(float(data['ask4p'])),int(data['ask4v'])],
        [abs(float(data['ask5p'])),int(data['ask5v'])]
    ]
    depth['bids']=[
        [abs(float(data['bid1p'])),int(data['bid1v'])],
        [abs(float(data['bid2p'])),int(data['bid2v'])],
        [abs(float(data['bid3p'])),int(data['bid3v'])],
        [abs(float(data['bid4p'])),int(data['bid4v'])],
        [abs(float(data['bid5p'])),int(data['bid5v'])]
    ]
    return depth

# -------------------------------------------------------------------------------------------
def get_tick_raw(code=None):
    t11 = time.time()
    df_ = get_allStock()
    innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
    if innerCode is None:
        return None
    url = "{}hq.niuguwang.com/aquote/quotedata/stocktransaction.ashx?code={}".format(pre,innerCode)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        if response.content.decode():
            response_ = '[' + response.content.decode().split('[')[1].split(']')[0] + ']'
            response_json = json.loads(response_)
            return fixing_tick(response_json)
        else:
            return pd.DataFrame()


def get_tick(code=None):
    delay_times = 5
    i = 0
    while i<delay_times:
        data = get_tick_raw(code=code)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data

        i+=1
        time.sleep(0.01)
        continue
    return pd.DataFrame()


def fixing_tick(data):
    df_data = pd.DataFrame(data)
    # print(df_data)
    trading_day = [str(datetime.datetime.strptime(str(i), '%Y%m%d%H%M%S')) for i in df_data['time']]
    df_data['time'] = trading_day
    return df_data


def get_allStock():
    sql_info = {
        'host':MYSQL_HOST,
        'port': MYSQL_PORT,
        'database': MYSQL_DATABASE,
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
    }
    try:
        sql = """select * from innerCodeMap;"""
        data = conn_mysql_select(sql,sql_info)
        if data:
            df_data = pd.DataFrame(data)
            df_data.columns = ['id', 'innercode', 'code', 'name', 'market','boardname','stocktype','insert_time','update_time']
            # df_data.columns = ['id', 'innercode', 'code', 'name', 'insert_time']
            # df_data.columns = ['id', 'innercode', 'code', 'name']
            return df_data
    except Exception:
        print(traceback.format_exc())


def get_allOnlyStock():
    sql_info = {
        'host':MYSQL_HOST,
        'port': MYSQL_PORT,
        'database': MYSQL_DATABASE,
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
    }
    try:
        sql = """select * from innerCodeMap where stocktype=1;"""
        data = conn_mysql_select(sql,sql_info)
        if data:
            df_data = pd.DataFrame(data)
            df_data.columns = ['id', 'innercode', 'code', 'name', 'market','boardname','stocktype','insert_time','update_time']
            # df_data.columns = ['id', 'innercode', 'code', 'name', 'insert_time']
            # df_data.columns = ['id', 'innercode', 'code', 'name']
            return df_data
    except Exception:
        print(traceback.format_exc())

def get_allStock2(date=None):
    # date_ = date.replace('-','')
    try:
        # 1 前复权
        url = "{}hq.niuguwang.com/aquote/quote/daykline_allstock.ashx?ex=0&date={}".format(pre, date)
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            return response_json['dayklines']
        else:
            return None

def inner2code(inner):
    try:
        url = "{}://pub.niuguwang.com/stockpub/stock/astockinfo.ashx?code={}".format(pre.split(':')[0],inner)
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            market = ''
            if response_json.get('market') == 1:
                market = 'SH'
            elif response_json.get('market') == 2:
                market = 'SZ'
            else:
                return None
            return response_json['symbol'] + '.' + market
        else:
            return None


def code2nameInner(code):
    try:
        url = "{}://pub.niuguwang.com/stockpub/stock/astockinfo.ashx?symbol={}".format(pre.split(':')[0],code)
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(response_json)
        if response_json:
            symbol = response_json['symbol']
            name = response_json['stockname']
            innercode = response_json['innercode']
            return [symbol,name,innercode]
        else:
            return None

# -------------------------------------------------------------------------------------------
def get_price_raw(codes=None):
    codes_list = []
    for code in codes:
        if isinstance(code,str):
            if len(code) == 9:
                code_s = code.split('.')[1].lower() + code.split('.')[0]
                codes_list.append(code_s)
            else:
                codes_list.append(code)
        if isinstance(code,int):
            codes_list.append(str(code))
    # codes_list = [str(i).split('.')[1].lower() + i.split('.')[0] for i in codes]
    codes_ = ','.join(codes_list)
    url = "{}hq.niuguwang.com/aquote/quotedata/batchstockprice.ashx?codes={}".format(pre,codes_)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        if response.content.decode():
            response_json = json.loads(response.content.decode())
            df_data = pd.DataFrame(response_json.get('list'))
            df_data['code'] = codes
            return df_data
        else:
            return pd.DataFrame()


def get_price(codes=None):
    delay_times = 5
    i = 0
    while i<delay_times:
        data = get_price_raw(codes=codes)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data

        i+=1
        time.sleep(0.01)
        continue
    return pd.DataFrame()

# ---------------------------------------------------------------------------------------------------
def get_allPlate():
    sql_info = {
        'host':SQL_SERVER_HOST,
        'database': SQL_SERVER_DATABASE,
        'user': SQL_SERVER_USER,
        'password': SQL_SERVER_PASSWORD,
    }
    sql = """select innerCode,Code,Name,PlateType,PlateId,SecuCategoryCodeII from PlateInfo;"""
    data = np.array(conn_sqlserver_select(sql,sql_info))
    df_data = pd.DataFrame(data,columns=['innercode', 'code', 'name', 'plate_type', 'plate_id', 'SecuCategoryCodeII'])
    df_data['stocktype'] = [2 for _ in range(len(df_data))]

    # plate_innerCode_list = df_data['innercode'].values
    # plate_code_list = df_data['code'].values

    return df_data


# ---------------------------------------------------------------------------------------------------------
def get_trans_raw(codes=None):
    codes_list = []
    for code in codes:
        if isinstance(code,str):
            if len(code) == 9:
                code_s = code.split('.')[1].lower() + code.split('.')[0]
                codes_list.append(code_s)
            else:
                codes_list.append(code)
        if isinstance(code,int):
            codes_list.append(str(code))
    # codes_list = [str(i).split('.')[1].lower() + i.split('.')[0] for i in codes]

    codes_ = ','.join(codes_list)
    url = "{}hq.niuguwang.com/aquote/quotedata/batchstockprice.ashx?codes={}&allpx=1&trans=1".format(pre,codes_)
    print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        if response.content.decode():
            response_json = json.loads(response.content.decode())
            df_data = pd.DataFrame(response_json.get('list'))
            df_data['code'] = codes
            return df_data
        else:
            return None


def get_trans(codes=None):
    delay_times = 5
    i = 0
    while i<delay_times:
        data = get_trans_raw(codes=codes)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data

        i+=1
        time.sleep(0.01)
        continue
# ---------------------------------------------------------------------------------------------------------
def get_zjlx():
    url = "http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=1.000001,0.399001&" \
          "fields=f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f64,f65,f70,f71,f76,f77,f82,f83,f164,f166,f168,f170,f172,f252,f253,f254,f255,f256,f124,f6,f278,f279,f280,f281,f282&" \
          "ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery18303224400345741254_1596166834140&_={}".format(round(time.time()*1000))
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        logger.info(traceback.format_exc())
    else:
        if response.content.decode():
            response_str = response.content.decode().split('(')[1].replace(')','').replace(';','')
            response_json = json.loads(response_str)

            zhuliJLR = 0
            chaodadanJLR = 0
            dadanJLR = 0
            zhongdanJLR = 0
            xiaodanJLR = 0
            for ss in response_json['data']['diff']:
                zhuliJLR += float(ss['f62'])
                chaodadanJLR += float(ss['f66'])
                dadanJLR += float(ss['f72'])
                zhongdanJLR += float(ss['f78'])
                xiaodanJLR += float(ss['f84'])
            return [zhuliJLR, chaodadanJLR, dadanJLR, zhongdanJLR, xiaodanJLR]
        else:
            return None



# -----------------------------------------------------------------------------------------------------------
def return_last_trading_day(date=None):
    if date:
        now_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        now_date = datetime.datetime.now()

    while True:
        l_date = now_date - datetime.timedelta(days=1)
        if is_trading_day(l_date):
            return l_date
        else:
            now_date = l_date
            continue



if __name__ == '__main__':
    import time
    from pprint import pprint

    # start_ = time.time()
    #
    # df = get_allStock()
    # print(df)
    #
    # innercode = df[df.code == '600747.SH']['innercode'].values[0]
    # name = df[df.code == '600747.SH']['name'].values[0]
    # print(innercode)
    # print(name)
    #
    #
    # print(time.time() - start_)
    #
    #
    # start_ = time.time()
    #
    # df = get_allPlate()
    # print(df)
    #
    # print(time.time() - start_)




    # start_ = time.time()
    #
    # data = get_plate_data_inner(code='882178', innercode=2000502, freq='d', adj='qfq', bars=300)
    # print(data)
    #
    # print(time.time() - start_)
    #
    #
    #
    #
    # start_ = time.time()
    #
    # data = get_plate_data_inner_raw(innercode=2000502, freq='d', adj='qfq', bars=300)
    # print(data)
    #
    # print(time.time() - start_)




    # start_ = time.time()
    #
    # data = get_stock_data_inner(code='000688.SH', innercode=2326, freq='d', adj='qfq', bars=300)
    # print(data)
    #
    # print(time.time() - start_)
    #
    #
    # start_ = time.time()
    #
    # data = get_stock_data_inner(code='399106.SZ', innercode=2194, freq='d', adj='qfq', bars=300)
    # print(data)
    #
    # print(time.time() - start_)




    # df = get_performance('2020-05-25')
    # print(df)

    # df = get_all_stock()
    # print(df)

    # df = get_dIndicesForValuation('2020-05-25')
    # print(df)

    # df = get_c_RR_ResearchReport(name='国泰君安', start='2020-05-10', end='2020-05-12')
    # print(df)

    # df = get_stock_basic(code='000058.SH')
    # pprint(df)

    # df = get_specialTrade()
    # print(df)

    # df = hk_hold('20190625')
    # print(df)

    # date = get_k_data(code='399006.SZ', freq='d', end='2020-07-05', bars=300)
    # print(date)
    # date = get_stock_data(code='399006.SZ', freq='d', adj='qfq',end='2020-07-05', bars=300)
    # print(date)

    # df = get_k_data(code='603106.SH', freq='d', start='2019-05-27', end='2020-07-08')
    # print(df)


    # data = get_stock_data(code='002982.SZ', freq='d', adj='qfq', start='2019-05-27', end='2020-07-08')
    # print(data)
    # 90762

    # # 分钟
    # data = get_stock_data(code='399006.SZ', freq='1m', adj='qfq', bars=300)
    # print(data)
    # data = get_stock_data(code='399006.SZ', freq='5m', adj='qfq', bars=300)
    # print(data)
    # data = get_stock_data(code='399006.SZ', freq='15m', adj='qfq', bars=300)
    # print(data)
    # data = get_stock_data(code='399006.SZ', freq='30m', adj='qfq', bars=300)
    # print(data)
    # data = get_stock_data(code='399006.SZ', freq='60m', adj='qfq', bars=300)
    # print(data)





    # data = get_stock_data(code='399006.SZ', freq='d', adj='qfq',end='2020-07-05', bars=300)
    # print(data)
    # data = get_stock_data(code='399006.SZ', freq='d', adj='qfq', start='2019-05-27', end='2020-07-08')
    # print(data)



    # data = get_stock_data(code='399006.SZ', freq='w', adj='qfq', bars=30)
    # print(data)
    # data = get_stock_data(code='399006.SZ', freq='mon', adj='qfq', bars=30)
    # print(data)


# code          trading_day   open   high    low  close  preclose          vol       value
#          code                 date   open   high    low  close  preclose       volume       value
#           code                 date   open   high    low  close  preclose       volume         value

    # # code
    # code_list = ["000858.SZ","600722.SH","000895.SZ","600006.SH"]
    # # table = 'QT_DailyQuote'
    # # field_list = ["TradingDay", "PrevClosePrice", "OpenPrice", "HighPrice", "LowPrice"]
    # table = 'LC_SHSZHSCHoldings'
    # field_list = ["SHSZHSCode", "SecuAbbr", "SharesHolding", "Holdratio", "InsertTime"]
    # body = {
    #     "table": table,
    #     "code_list": code_list,
    #     # "all_code": True,
    #     "field_list": field_list,
    #     # "alterField": "TradingDay",
    #     "alterField": "EndDate",
    #     "startDate": "2020-01-23",
    #     "endDate": "2020-05-26"
    # }
    # data = get_fromCode(body)
    # print(data)


    # company
    # code_list = ["000858.SZ", "600722.SH", "000895.SZ", "600006.SH"]
    # table = 'LC_MainQuarterData'
    # field_list = ["EndDate", "BasicEPS", "OperatingReenue", "CashEquialents", "TotalShares"]
    # body = {
    #     "table": table,
    #     "code_list": code_list,
    #     # "all_code": True,
    #     "field_list": field_list,
    #     "alterField": "EndDate",
    #     "startDate": "2019-01-01",
    #     "endDate": "2020-05-26"
    # }
    # data = get_fromCompany(body)
    # print(data)
    #
    #
    #
    # # date
    # table = 'QT_SHSZHSCTradingDay'
    # field_list = ["EndDate", "TradingType", "IfWeekEnd", "IfYearEnd", "UpdateTime","InfoSource"]
    # body = {
    #     "table": table,
    #     "field_list": field_list,
    #     "alterField": "EndDate",
    #     "startDate": "2020-01-01",
    #     "endDate": "2020-05-26"
    # }
    # data = get_fromDate(body)
    # pprint(data)









    # depth = get_depth(code='000028.SZ')
    # pprint(depth)
    # print(depth['asks'][1][0])
    # print(depth['asks'][0][0])
    #
    #
    # tick = get_tick(code='000028.SZ')
    # print(tick)
    #
    #
    #
    # table = 'C_RR_ResearchReport'
    # field_list = ["OrgName", "OrgNameDisc", "AreaCode", "Author", "WritingDate", "InsertTime"]
    # name = ['国泰君安', '中信证券']
    #
    # body = {
    #     "table": table,
    #     "field_list": field_list,
    #     "alterFieldName": "OrgNameDisc",
    #     "name":name,
    #     "alterFieldDate": "InfoPublDate",
    #     "startDate": "2020-05-01",
    #     "endDate": "2020-07-07"
    # }
    # data = get_fromDateName(body=body)
    # print(data)



    # price = get_price(codes=['000001.SZ','600000.SH','000028.SZ',"000858.SZ", "600722.SH", "000895.SZ", "600006.SH"])
    # print(price)

    a = code2nameInner('300033')
    print(a)
    # print(time.time()-start_)



