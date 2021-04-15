import hashlib
import time
import random
import json
import traceback
import requests
import datetime
import pandas as pd
import numpy as np
from ngwshare.conn_db.conn_sqlserver import conn_sqlserver_select,conn_sqlserver_insert
from ngwshare.conn_db.conn_mysql import conn_mysql_select
from ngwshare.utils.date_util import str2datetime, get_date_length, is_trading_day, get_date_min_length
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
from ngwshare.constants import (
    MYSQL_2_HOST,
    MYSQL_2_PORT,
    MYSQL_2_DATABASE,
    MYSQL_2_USER,
    MYSQL_2_PASSWORD
)

from ngwshare.data.us_data import *
from ngwshare.data.contract_guba import *
from ngwshare.data.contract_extra import *
from ngwshare.data.statistics_data import *
from ngwshare.data.factor import *

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

host = HOST
pre = PRE
requests.DEFAULT_RETRIES = 10

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import hmac
import hashlib
import base64
import urllib.parse


def send_mail_raw(to_addr=None, header=None, content=None):
    # # 发信人
    # from_addr = '969282488@qq.com'
    # token = 'kpofdicliftibfcc'
    # 发信人
    # from_addr = '296348304@qq.com'
    # token = 'jrhflcppohwsbjfj'

    r_num = random.randint(1, 2)
    from_dict = {1:['969282488@qq.com','kpofdicliftibfcc'],2:['296348304@qq.com','jrhflcppohwsbjfj']}
    from_addr = from_dict[r_num][0]
    token = from_dict[r_num][1]

    # 收信方邮箱
    # to_addr = '296348304@qq.com'
    # to_addr = 'wj296348304@163.com'

    # 发信服务器
    smtp_server = 'smtp.qq.com'
    try:
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(content, 'plain', 'utf-8')
        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(header)

        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        server.login(from_addr, token)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        return True
    except:
        print(traceback.format_exc())
        return False


def send_mail(to_addr=None, header=None, content=None):
    delay_times = 10
    i = 0
    while i < delay_times:
        # print(i)
        flag = send_mail_raw(to_addr=to_addr, header=header, content=content)
        if flag:
            return True
        i += 1
        time.sleep(30)
        continue
    return False


def sent_dingding_raw(content=None,mobile=None,is_all=None):
    # body = {
    #         "msgtype": "text",
    #         "text": {"content": content},
    #         "at": {"atMobiles": ["13087005272"],"isAtAll": True}
    # }
    body = {
            "msgtype": "text",
            "text": {"content": content},
            "at": {"atMobiles": mobile,"isAtAll": is_all}
    }
    timestamp = str(round(time.time() * 1000))
    # secret = 'SEC375f38f420fef0605b585e40990f34aee2191316a8a995ee66584990b1cbf2f0'
    secret = 'SEC89e9edf6f74e2e03a0e055b58cf575f35b66a8e5a7939611f9f9c3acaa2b11f8'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    # url = 'https://oapi.dingtalk.com/robot/send?access_token=8410e2c656a9b99c984896c7970bab3e860473995d3f9128938c3e5d82d63151' \
    #       '&timestamp={}&sign={}'.format(timestamp,sign)
    url = 'https://oapi.dingtalk.com/robot/send?access_token=20ecf2ff2422c67be8c72b937a7348fb0e64ffaaba7d83b577578a5c2f8a17c8' \
          '&timestamp={}&sign={}'.format(timestamp,sign)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        if response_json['errcode'] == 0:
            return True
        else:
            return False
    except Exception:
        print(traceback.format_exc())
        return False

def sent_dingding(content=None,mobile=None,is_all=None):
    delay_times = 10
    i = 0
    while i < delay_times:
        # print(i)
        flag = sent_dingding_raw(content=content,mobile=mobile,is_all=is_all)
        if flag:
            return True
        i += 1
        time.sleep(30)
        continue
    return False







def sent_dingding_raw2(content=None,mobile=None,is_all=None):
    # body = {
    #         "msgtype": "text",
    #         "text": {"content": content},
    #         "at": {"atMobiles": ["13087005272"],"isAtAll": True}
    # }
    body = {
            "msgtype": "text",
            "text": {"content": content},
            "at": {"atMobiles": mobile,"isAtAll": is_all}
    }
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC375f38f420fef0605b585e40990f34aee2191316a8a995ee66584990b1cbf2f0'
    # secret = 'SEC89e9edf6f74e2e03a0e055b58cf575f35b66a8e5a7939611f9f9c3acaa2b11f8'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    url = 'https://oapi.dingtalk.com/robot/send?access_token=8410e2c656a9b99c984896c7970bab3e860473995d3f9128938c3e5d82d63151' \
          '&timestamp={}&sign={}'.format(timestamp,sign)
    # url = 'https://oapi.dingtalk.com/robot/send?access_token=20ecf2ff2422c67be8c72b937a7348fb0e64ffaaba7d83b577578a5c2f8a17c8' \
    #       '&timestamp={}&sign={}'.format(timestamp,sign)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        if response_json['errcode'] == 0:
            return True
        else:
            return False
    except Exception:
        print(traceback.format_exc())
        return False

def sent_dingding2(content=None,mobile=None,is_all=None):
    delay_times = 10
    i = 0
    while i < delay_times:
        # print(i)
        flag = sent_dingding_raw2(content=content,mobile=mobile,is_all=is_all)
        if flag:
            return True
        i += 1
        time.sleep(30)
        continue
    return False


def get_k_data(code=None, freq=None, start=None, end=None, bars=None):
    if bars:
        len = 200 if bars < 100 else 500
        start = str(str2datetime(end) - datetime.timedelta(days=bars + len))
        # print(start,end)
    try:
        headers = {'User-Agent': get_ua()}
        url = "http://{}/api/dailyQuote?secuCodeMarket={}&startDate={}&endDate={}" \
            .format(host, code, start, end)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        headers = {'User-Agent': get_ua()}
        url = "http://{}/api/stockBasic?secuCodeMarket={}".format(host, code)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            return response_json['data']
        else:
            return None


def get_all_stock():
    try:  # http://192.168.8.104:3389/api/stockAll
        headers = {'User-Agent': get_ua()}
        url = "http://{}/api/stockAll".format(host)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        headers = {'User-Agent': get_ua()}
        url = "http://{}/api/performance?date={}".format(host, date)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        headers = {'User-Agent': get_ua()}
        url = "http://{}/api/dIndicesForValuation?date={}".format(host, date)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            df_data.columns = ['code', 'name', 'date', 'PELYR', 'PE', 'PB', 'PCF', 'PS', 'InsertTime']
            return df_data
        else:
            return None


def get_c_RR_ResearchReport(name=None, start=None, end=None):
    try:
        headers = {'User-Agent': get_ua()}
        url = "http://{}/api/c_RR_ResearchReport?name={}&startDate={}&endDate={}" \
            .format(host, name, start, end)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            return df_data
        else:
            return None


def get_specialTrade():
    try:
        headers = {'User-Agent': get_ua()}
        url = "http://{}/api/specialTrade".format(host)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            df_data.columns = ['code', 'name', 'date', 'type']
            return df_data
        else:
            return None


def get_financialData(table, stock, filed_list, start, end):
    if len(stock) > 1:
        stock = tuple(stock)
    else:
        stock = str(tuple(stock)).replace(',', '')
    try:
        url = "http://{}/api/financialData?table={}&code={}&field={}&startDate={}&endDate={}" \
            .format(host, table, stock, filed_list, start, end)
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            return df_data
        else:
            return None


def get_financialDataPro(table, alterFiled, filed_list, start, end):
    try:
        url = "http://{}/api/newestFinaIndex?table={}&alterField={}&field={}&startDate={}&endDate={}" \
            .format(host, table, alterFiled, filed_list, start, end)
        headers = {"Content-Type": "application/json",
                   'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        url = "http://{}/api/fromCode".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        url = "http://{}/api/fromCompany".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        url = "http://{}/api/fromDate".format(host)
        # print(url)
        # print(body)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        url = "http://{}/api/fromDateName".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        url = "http://{}/api/fromTable".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        url = "http://{}/api/fromName".format(host)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
    if freq in ['1m','1Min','1min','1Minute','1minute']:
        return 11
    if freq in ['5m','5Min','5min','5Minute','5minute']:
        return 1
    if freq in ['15m','15Min','15min','15Minute','15minute']:
        return 2
    if freq in ['30m','30Min','30min','30Minute','30minute']:
        return 3
    if freq in ['60m','60Min','60min','60Minute','60minute']:
        return 4
    if freq in ['d', 'day', 'DAY', 'Day', '1d']:
        return 5
    if freq in ['w','week','1w','1week','1W','1Week']:
        return 6
    if freq in ['mon','month','1mon','1Month']:
        return 9


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
    # value = [round(float(i), 4) for i in df_data['curvalue']]

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


def fixing_k_data_mm(data):
    df_data = pd.DataFrame(data)
    df_data = df_data[['innercode', 'highp', 'openp', 'lowp', 'nowv', 'curvol', 'curvalue']]
    innercode = [int(i) for i in df_data['innercode']]
    high = [round(float(i) / 100, 4) for i in df_data['highp']]
    open = [round(float(i) / 100, 4) for i in df_data['openp']]
    low = [round(float(i) / 100, 4) for i in df_data['lowp']]
    close = [round(float(i) / 100, 4) for i in df_data['nowv']]
    vol = [round(float(i), 4) for i in df_data['curvol']]
    # value = [round(float(i), 4) for i in df_data['curvalue']]

    data_dict = {}
    data_dict['innercode'] = innercode
    data_dict['open'] = open
    data_dict['high'] = high
    data_dict['low'] = low
    data_dict['close'] = close
    data_dict['volume'] = vol
    data_dict['value'] = df_data['curvalue']
    df_data_ = pd.DataFrame(data_dict)
    return df_data_



def fixing_stock_min_data(data,code,start,end,bars,freq):
    df_data = pd.DataFrame(data)
    data_dict = {}
    data_dict['code'] = [code for _ in range(len(df_data))]
    data_dict['date'] = [str(datetime.datetime.strptime(str(i), '%Y%m%d%H%M%S')) for i in df_data['times']]
    data_dict['open'] = [round(float(i) / 100, 4) for i in df_data['openp']]
    data_dict['high'] = [round(float(i) / 100, 4) for i in df_data['highp']]
    data_dict['low'] = [round(float(i) / 100, 4) for i in df_data['lowp']]
    data_dict['close'] = [round(float(i) / 100, 4) for i in df_data['nowv']]
    data_dict['preclose'] = [round(float(i) / 100, 4) for i in df_data['preclose']]
    data_dict['volume'] = [int(i) for i in df_data['curvol']]
    data_dict['value'] =  [int(i) for i in df_data['curvalue']]
    df_data_ = pd.DataFrame(data_dict)
    if (not start) and (not end) and bars:
        return df_data_.sort_values(by='date').reset_index(drop=True)
    else:
        if bars:
            if len(end) == 10:
                end += ' 23:59:59'
            df_data_n = df_data_.loc[(df_data_["date"] <= end)]
            df_data_n = df_data_n.sort_values(by='date').reset_index(drop=True)
            df_data_n = df_data_n[-bars:].reset_index(drop=True)
            return df_data_n
        else:
            if len(start) == 10:
                start += ' 00:00:00'
            if len(end) == 10:
                end += ' 23:59:59'
            if freq in ['1m', '1Min', '1min', '1Minute', '1minute']:
                df_data_n = df_data_.loc[(df_data_["date"] >= start) & (df_data_["date"] < end)]
            else:
                df_data_n = df_data_.loc[(df_data_["date"] >= start) & (df_data_["date"] <= end)]
            return df_data_n.sort_values(by='date').reset_index(drop=True)




def get_stock_data_raw(code=None, innercode=None, freq=None, adj=None, start=None, end=None, bars=None):
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
        len = 200 if bars < 100 else 500
        start = str(str2datetime(end) - datetime.timedelta(days=bars + len))
        if get_type_from_freq(freq) in [6]:
            len = 3000
            start = str(str2datetime(end) - datetime.timedelta(days=bars + len))
        if get_type_from_freq(freq) in [9]:
            len = 10000
            start = str(str2datetime(end) - datetime.timedelta(days=bars + len))

    if innercode is None:
        df_ = get_allStock()
        try:
            innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
        except:
            return pd.DataFrame()
        # print(innerCode)
        if innerCode is None:
            return pd.DataFrame()
    else:
        innerCode = innercode

    count = get_date_length(start, end)  # 开始日期到目前截至日期的len
    # print(count)
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
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(response_json)
        # print(time.time()-t)
        if response_json:
            data = response_json['timedata']
            # print(data)
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


def get_stock_data_raw_m(code=None, innercode=None, freq=None, adj=None, start=None, end=None, bars=None):
    """
    :param code: 证券代码
    :param freq: 频率  1m  5m  15m  30m  60m  d   w   month
    :param adj: 复权类型  None：不复权（除权）   qfq：前复权    hfq：后复权
    :param start: 开始日期
    :param end: 结束日期
    :return:
    """
    # inner_code_dict
    if innercode is None:
        df_ = get_allStock()
        try:
            innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
        except:
            return pd.DataFrame()
        # print(innerCode)
        if innerCode is None:
            return pd.DataFrame()
    else:
        innerCode = innercode

    type = get_type_from_freq(freq)
    ex = get_ex_from_adj(adj)
    url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}&ex={}" \
        .format(pre, innerCode, type, bars, ex)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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


def get_stock_data_min_raw(code=None, innercode=None, freq=None, adj=None, start=None, end=None, bars=None):
    if innercode is None:
        df_ = get_allStock()
        try:
            innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
        except:
            return pd.DataFrame()
        if innerCode is None:
            return pd.DataFrame()
    else:
        innerCode = innercode
    # print(innerCode)
    ex = get_ex_from_adj(adj)
    type = get_type_from_freq(freq)

    if (not start) and (not end) and bars:
        count = bars
        if ex:
            url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}&ex={}".format(pre, innerCode, type, count, ex)
        else:
            url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}".format(pre, innerCode, type, count)
    else:
        if bars:
            count = bars+100
            if freq in ['1m', '1Min', '1min', '1Minute', '1minute']:
                end_ = str(str2datetime(end) + datetime.timedelta(minutes=1))
            elif freq in ['5m', '5Min', '5min', '5Minute', '5minute']:
                end_ = str(str2datetime(end) + datetime.timedelta(minutes=5))
            elif freq in ['15m', '15Min', '15min', '15Minute', '15minute']:
                end_ = str(str2datetime(end) + datetime.timedelta(minutes=15))
            elif freq in ['30m', '30Min', '30min', '30Minute', '30minute']:
                end_ = str(str2datetime(end) + datetime.timedelta(minutes=30))
            elif freq in ['60m', '60Min', '60min', '60Minute', '60minute']:
                end_ = str(str2datetime(end) + datetime.timedelta(minutes=60))
            else:
                end_ = str(str2datetime(end) + datetime.timedelta(minutes=60))
            if len(end) == 10:
                end_ = str(str2datetime(end) + datetime.timedelta(days=1))
            start_ = end_.replace('-', '').replace(':', '').replace(' ', '')
        else:
            count = get_date_min_length(start, end, freq)  # 开始日期到目前截至日期的len
            end_ = str(str2datetime(end) + datetime.timedelta(days=1))
            start_ = end_.replace('-', '').replace(':', '').replace(' ', '')
        if ex:
            url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&start={}&count={}&ex={}" \
                .format(pre, innerCode, type, start_, count, ex)
        else:
            url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&start={}&count={}" \
                .format(pre, innerCode, type, start_, count)
    # print(url)
    try:
        # t = time.time()
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            if response_json:
                data = response_json['timedata']
                if data:
                    df_data = fixing_stock_min_data(data,code,start,end,bars,freq)
                    return df_data
                else:
                    # print('休市.')
                    return pd.DataFrame()
            else:
                return pd.DataFrame()
        except:
            return pd.DataFrame()



def get_stock_data(code=None, freq=None, adj=None, start=None, end=None, bars=None, innercode=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        # print(i,delay_times)
        data = pd.DataFrame()
        if freq in ['d', 'day', 'DAY', 'Day', '1d', 'w', 'week', '1w', '1week', '1W', '1Week','mon', 'month', '1mon', '1Month' ]:
            if (end and bars) or (start and end):
                data = get_stock_data_raw(code=code, innercode=innercode, freq=freq, adj=adj, start=start, end=end,bars=bars)
            elif end is None and bars:
                data = get_stock_data_raw_m(code=code, innercode=innercode, freq=freq, adj=adj, start=start, end=end,bars=bars)
            else:
                return pd.DataFrame()
        elif freq in ['1m', '1Min', '1min', '1Minute', '1minute',
                      '5m', '5Min', '5min', '5Minute', '5minute',
                      '15m', '15Min', '15min', '15Minute', '15minute',
                      '30m', '30Min', '30min', '30Minute', '30minute',
                      '60m', '60Min', '60min', '60Minute', '60minute']:
            data = get_stock_data_min_raw(code=code, freq=freq, adj=adj, start=start, end=end, bars=bars,innercode=innercode)
        else:
            return data

        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue

    return pd.DataFrame()


# def get_stock_data(code=None, freq=None, adj=None, start=None, end=None, bars=None, innercode=None):
#     delay_times = 5
#     i = 0
#     while i < delay_times:
#         # print(i,delay_times)
#         data = pd.DataFrame()
#         if (end and bars) or (start and end):
#             data = get_stock_data_raw(code=code, innercode=innercode, freq=freq, adj=adj, start=start, end=end,
#                                       bars=bars)
#         elif end is None and bars:
#             data = get_stock_data_raw_m(code=code, innercode=innercode, freq=freq, adj=adj, start=start, end=end,
#                                         bars=bars)
#         else:
#             return pd.DataFrame()
#
#         if isinstance(data, pd.DataFrame):
#             if not data.empty:
#                 return data
#
#         i += 1
#         time.sleep(0.01)
#         continue
#     return pd.DataFrame()


# ------------------------------------------------------------------------------------------


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
        print(traceback.format_exc())
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
        print(traceback.format_exc())
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
def get_plate_data_inner_rr(code=None, innercode=None, freq=None, adj=None, bars=None, start=None, end=None):
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

    url = ''
    if end and bars:
        end_ = str(str2datetime(end) + datetime.timedelta(days=1))
        start_ = end_.replace('-', '').replace(':', '').replace(' ', '')
        count = bars
        url = "{}hq.niuguwang.com/aquote/plate/kline.ashx?code={}&type={}&count={}&ex={}&start={}" \
            .format(pre, innercode, type, count, ex, start_)
    if start and end and bars is None:
        count = get_date_length(start, end)  # 开始日期到目前截至日期的len
        end_ = str(str2datetime(end) + datetime.timedelta(days=1))
        start_ = end_.replace('-', '').replace(':', '').replace(' ', '')
        url = "{}hq.niuguwang.com/aquote/plate/kline.ashx?code={}&type={}&count={}&ex={}&start={}" \
            .format(pre, innercode, type, count, ex, start_)
    if end is None and bars:
        url = "{}hq.niuguwang.com/aquote/plate/kline.ashx?code={}&type={}&count={}&ex={}" \
            .format(pre, innercode, type, bars, ex)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(response_json)
        if response_json:
            data = response_json['timedata']
            if data:
                # print(data)
                if start and end and bars is None:
                    df_data = fixing_k_data(data, code, start, end)
                else:
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
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            data = response_json['timedata']
            df_data = pd.DataFrame(data)
            return df_data
        else:
            return pd.DataFrame()


def get_plate_data_inner(code=None, innercode=None, freq=None, adj=None, bars=None, start=None, end=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = pd.DataFrame()
        if (end and bars) or (start and end):
            data = get_plate_data_inner_rr(code=code, innercode=innercode, freq=freq, adj=adj, start=start, end=end,
                                           bars=bars)
        elif end is None and bars:
            data = get_plate_data_inner_rr(code=code, innercode=innercode, freq=freq, adj=adj, start=start, end=end,
                                           bars=bars)
        else:
            return pd.DataFrame()
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data

        i += 1
        time.sleep(0.01)
        continue
    return pd.DataFrame()


# -------------------------------------------------------------------------------------------
# 获取深度信息
def get_depth_raw(code=None):
    df_ = get_allStock()
    innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
    if innerCode is None:
        return None
    url = "{}hq.niuguwang.com/aquote/quotedata/detailfivedish.ashx?code={}".format(pre, innerCode)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(time.time()-t)
        if response_json:
            return fixing_depth(response_json, code)
        else:
            return None


def get_depth(code=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_depth_raw(code=code)
        if data:
            return data

        i += 1
        time.sleep(0.01)
        continue


def fixing_depth(data, code):
    depth = {}
    depth['time'] = str(datetime.datetime.strptime(str(data['time']), '%Y%m%d%H%M%S'))
    depth['code'] = code
    depth['asks'] = [
        [abs(float(data['ask1p'])), int(data['ask1v'])],
        [abs(float(data['ask2p'])), int(data['ask2v'])],
        [abs(float(data['ask3p'])), int(data['ask3v'])],
        [abs(float(data['ask4p'])), int(data['ask4v'])],
        [abs(float(data['ask5p'])), int(data['ask5v'])]
    ]
    depth['bids'] = [
        [abs(float(data['bid1p'])), int(data['bid1v'])],
        [abs(float(data['bid2p'])), int(data['bid2v'])],
        [abs(float(data['bid3p'])), int(data['bid3v'])],
        [abs(float(data['bid4p'])), int(data['bid4v'])],
        [abs(float(data['bid5p'])), int(data['bid5v'])]
    ]
    return depth


# -------------------------------------------------------------------------------------------
def get_tick_raw(code=None):
    t11 = time.time()
    df_ = get_allStock()
    innerCode = df_[df_['code'] == code]['innercode'].tolist()[0]
    if innerCode is None:
        return None
    url = "{}hq.niuguwang.com/aquote/quotedata/stocktransaction.ashx?code={}".format(pre, innerCode)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
    while i < delay_times:
        data = get_tick_raw(code=code)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data

        i += 1
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


def get_allStockNew():
    try:
        headers = {'User-Agent': get_ua()}
        url = "https://stq.niuguwang.com/ft/innercode"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            return df_data
        else:
            return None


# def get_allStock():
#     sql_info = {
#         'host':MYSQL_HOST,
#         'port': MYSQL_PORT,
#         'database': MYSQL_DATABASE,
#         'user': MYSQL_USER,
#         'password': MYSQL_PASSWORD,
#     }
#     try:
#         sql = """select * from innerCodeMap;"""
#         data = conn_mysql_select(sql,sql_info)
#         if data:
#             df_data = pd.DataFrame(data)
#             df_data.columns = ['id', 'innercode', 'code', 'name', 'market','boardname','stocktype','insert_time','update_time']
#             # df_data.columns = ['id', 'innercode', 'code', 'name', 'insert_time']
#             # df_data.columns = ['id', 'innercode', 'code', 'name']
#             return df_data
#     except Exception:
#         print(traceback.format_exc())


def get_allOnlyStock():
    sql_info = {
        'host': MYSQL_HOST,
        'port': MYSQL_PORT,
        'database': MYSQL_DATABASE,
        'user': MYSQL_USER,
        'password': MYSQL_PASSWORD,
    }
    try:
        sql = """select * from innerCodeMap where stocktype=1;"""
        data = conn_mysql_select(sql, sql_info)
        if data:
            df_data = pd.DataFrame(data)
            df_data.columns = ['id', 'innercode', 'code', 'name', 'market', 'boardname', 'stocktype', 'insert_time',
                               'update_time']
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
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            return response_json['dayklines']
        else:
            return None


def get_allStockData(adj=None, date=None):
    date_ = date.replace('-', '')
    ex = get_ex_from_adj(adj)
    try:
        # 1 前复权
        url = "{}hq.niuguwang.com/aquote/quote/daykline_allstock.ashx?ex={}&date={}".format(pre, ex, date_)
        # print(url)
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            df_data = fixing_k_data_mm(response_json['dayklines'])
            return df_data
        else:
            return None


def inner2code(inner):
    try:
        url = "{}://pub.niuguwang.com/stockpub/stock/astockinfo.ashx?code={}".format(pre.split(':')[0], inner)
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
        url = "{}://pub.niuguwang.com/stockpub/stock/astockinfo.ashx?symbol={}".format(pre.split(':')[0], code)
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(response_json)
        if response_json:
            symbol = response_json['symbol']
            name = response_json['stockname']
            innercode = response_json['innercode']
            return [symbol, name, innercode]
        else:
            return None


# -------------------------------------------------------------------------------------------
def get_price_raw(codes=None):
    codes_list = []
    for code in codes:
        if isinstance(code, str):
            if len(code) == 9:
                code_s = code.split('.')[1].lower() + code.split('.')[0]
                codes_list.append(code_s)
            else:
                codes_list.append(code)
        if isinstance(code, int):
            codes_list.append(str(code))
    # codes_list = [str(i).split('.')[1].lower() + i.split('.')[0] for i in codes]
    codes_ = ','.join(codes_list)
    url = "{}hq.niuguwang.com/aquote/quotedata/batchstockprice.ashx?codes={}".format(pre, codes_)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
    while i < delay_times:
        data = get_price_raw(codes=codes)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data

        i += 1
        time.sleep(0.01)
        continue
    return pd.DataFrame()


# ---------------------------------------------------------------------------------------------------
# 基金
# def get_all_funds():
#     sql_info = {
#         'host': SQL_SERVER_HOST,
#         'database': SQL_SERVER_DATABASE,
#         'user': SQL_SERVER_USER,
#         'password': SQL_SERVER_PASSWORD,
#     }
#     sql = """select InnerCode,TradingCode,SecuAbbr,ChiSpelling,SecuCategory,SecuCategoryCodeII,ExchangeCode,ExchangeName
#     from SECURITIES_INNERCODE where SecuCategoryCodeII in (1003,1004,1005) and ListingStateCode=1;"""
#     # print(sql)
#     data = np.array(conn_sqlserver_select(sql, sql_info))
#     df_data = pd.DataFrame(data, columns=['InnerCode', 'TradingCode', 'SecuAbbr', 'ChiSpelling', 'SecuCategory',
#                                           'SecuCategoryCodeII','ExchangeCode','ExchangeName'])
#     df_data['TradingCode'] = [(dict(df_data.loc[i])['TradingCode'] + ('.SH' if int(dict(df_data.loc[i])['ExchangeCode']) == 101 else '.SZ')) for i in df_data.index]
#     return df_data


def get_all_funds():
    try:
        headers = {'User-Agent': get_ua()}
        url = "https://stq.niuguwang.com/ft/funds"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            return df_data
        else:
            return None



def fixing_fund_data(data=None,code=None,is_start_end=None,start=None,end=None):
    df_data = pd.DataFrame(data)
    df_data = df_data[['times', 'highp', 'openp', 'lowp', 'nowv', 'preclose', 'curvol', 'curvalue']]
    trading_day = [str(datetime.datetime.strptime(str(i), '%Y%m%d%H%M%S'))[:19] for i in df_data['times']]
    high = [round(float(i) / 100, 4) for i in df_data['highp']]
    open = [round(float(i) / 100, 4) for i in df_data['openp']]
    low = [round(float(i) / 100, 4) for i in df_data['lowp']]
    close = [round(float(i) / 100, 4) for i in df_data['nowv']]
    preclose = [round(float(i) / 100, 4) for i in df_data['preclose']]
    vol = [int(i) for i in df_data['curvol']]
    value = [int(i) for i in df_data['curvalue']]

    data_dict = {}
    data_dict['code'] = [code for _ in range(len(trading_day))]
    data_dict['date'] = trading_day
    data_dict['open'] = open
    data_dict['high'] = high
    data_dict['low'] = low
    data_dict['close'] = close
    data_dict['preclose'] = preclose
    data_dict['volume'] = vol
    data_dict['value'] = value
    df_data_ = pd.DataFrame(data_dict)

    if is_start_end:
        if len(start) == 10:
            start += ' 00:00:00'
        if len(end) == 10:
            end += ' 00:00:00'
        df_data_n = df_data_.loc[(df_data_["date"] >= start) & (df_data_["date"] <= end)]
        return df_data_n.sort_values(by='date').reset_index(drop=True)
    else:
        return df_data_.sort_values(by='date')



def get_fund_data_raw(code=None, innercode=None, freq=None, adj=None, start=None, end=None, bars=None):
    type = get_type_from_freq(freq)
    ex = get_ex_from_adj(adj)
    if innercode is None:
        df_ = get_all_funds()
        try:
            innercode_ = df_[df_['TradingCode'] == int(code.split('.')[0])]['InnerCode'].tolist()[0]
        except:
            return pd.DataFrame()
        if innercode_ is None:
            return pd.DataFrame()
    else:
        innercode_ = innercode

    url = ''
    is_start_end = False
    if bars and not start and not end:
        url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}&ex={}" \
            .format(pre, innercode_, type, bars, ex)
    if bars and not start and end:
        end_ = str(str2datetime(end) + datetime.timedelta(days=1))
        end__ = end_.replace('-', '').replace(':', '').replace(' ', '')
        url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}&start={}&ex={}" \
            .format(pre, innercode_, type, bars, end__, ex)
    if not bars and start and end:
        is_start_end = True
        end_ = str(str2datetime(end) + datetime.timedelta(days=1))
        end__ = end_.replace('-', '').replace(':', '').replace(' ', '')
        bars_ = get_date_length(start, end)
        url = "{}hq.niuguwang.com/aquote/quote/kline.ashx?code={}&type={}&count={}&start={}&ex={}" \
            .format(pre, innercode_, type, bars_, end__, ex)
    # print(url)
    try:
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json:
            data = response_json['timedata']
            return fixing_fund_data(data,code,is_start_end,start,end)
        else:
            return pd.DataFrame()


def get_fund_data(code=None, innercode=None, freq=None, adj=None, start=None, end=None, bars=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_fund_data_raw(code=code, innercode=innercode, freq=freq, adj=adj, start=start, end=end, bars=bars)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue
    return pd.DataFrame()


# 获取基金深度信息
def get_funds_depth_raw(code=None,innercode=None):
    if not innercode:
        df_ = get_all_funds()
        innercode_ = df_[df_['TradingCode'] == code]['InnerCode'].tolist()[0]
        if innercode_ is None:
            return None
    else:
        innercode_ = innercode

    url = "{}hq.niuguwang.com/aquote/quotedata/detailfivedish.ashx?code={}".format(pre, innercode_)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        # print(time.time()-t)
        if response_json:
            return fixing_funds_depth(response_json, code)
        else:
            return None


def get_funds_depth(code=None,innercode=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_funds_depth_raw(code=code,innercode=innercode)
        if data:
            return data

        i += 1
        time.sleep(0.01)
        continue


def fixing_funds_depth(data, code):
    depth = {}
    depth['time'] = str(datetime.datetime.strptime(str(data['time']), '%Y%m%d%H%M%S'))
    depth['code'] = code
    depth['asks'] = [
        [abs(float(data['ask1p'])), int(data['ask1v'])],
        [abs(float(data['ask2p'])), int(data['ask2v'])],
        [abs(float(data['ask3p'])), int(data['ask3v'])],
        [abs(float(data['ask4p'])), int(data['ask4v'])],
        [abs(float(data['ask5p'])), int(data['ask5v'])]
    ]
    depth['bids'] = [
        [abs(float(data['bid1p'])), int(data['bid1v'])],
        [abs(float(data['bid2p'])), int(data['bid2v'])],
        [abs(float(data['bid3p'])), int(data['bid3v'])],
        [abs(float(data['bid4p'])), int(data['bid4v'])],
        [abs(float(data['bid5p'])), int(data['bid5v'])]
    ]
    return depth


# ---------------------------------------------------------------------------------------------------
# 行业
# def get_allPlate():
#     sql_info = {
#         'host': SQL_SERVER_HOST,
#         'database': SQL_SERVER_DATABASE,
#         'user': SQL_SERVER_USER,
#         'password': SQL_SERVER_PASSWORD,
#     }
#     sql = """select innerCode,Code,Name,PlateType,PlateId,SecuCategoryCodeII from PlateInfo;"""
#     data = np.array(conn_sqlserver_select(sql, sql_info))
#     df_data = pd.DataFrame(data, columns=['innercode', 'code', 'name', 'plate_type', 'plate_id', 'SecuCategoryCodeII'])
#     df_data['stocktype'] = [2 for _ in range(len(df_data))]
#
#     # plate_innerCode_list = df_data['innercode'].values
#     # plate_code_list = df_data['code'].values
#
#     return df_data


def get_allPlate():
    try:
        headers = {'User-Agent': get_ua()}
        url = "https://stq.niuguwang.com/ft/plates"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        response_json = json.loads(response.content.decode())
        if response_json["resultCode"] == 0:
            df_data = pd.DataFrame(response_json['data'])
            return df_data
        else:
            return None



# ---------------------------------------------------------------------------------------------------------
def get_trans_raw(codes=None):
    codes_list = []
    for code in codes:
        if isinstance(code, str):
            if len(code) == 9:
                code_s = code.split('.')[1].lower() + code.split('.')[0]
                codes_list.append(code_s)
            else:
                codes_list.append(code)
        if isinstance(code, int):
            codes_list.append(str(code))
    # codes_list = [str(i).split('.')[1].lower() + i.split('.')[0] for i in codes]

    codes_ = ','.join(codes_list)
    url = "{}hq.niuguwang.com/aquote/quotedata/batchstockprice.ashx?codes={}&allpx=1&trans=1".format(pre, codes_)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
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
    while i < delay_times:
        data = get_trans_raw(codes=codes)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data

        i += 1
        time.sleep(0.01)
        continue


# ---------------------------------------------------------------------------------------------------------
def get_turnover_raw(inner_list=None):
    inner_list = [str(i) for i in inner_list]
    inner_list_str = ','.join(inner_list)

    url = "{}hq.niuguwang.com/aquote/quote/abatchquote.ashx?code={}".format(pre, inner_list_str)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        if response.content.decode():
            response_json = json.loads(response.content.decode())
            df_data = pd.DataFrame(response_json.get('list'))
            return df_data
        else:
            return None


def get_turnover(inner_list=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_turnover_raw(inner_list=inner_list)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue


# ---------------------------------------------------------------------------------------------------------
def get_zjlx():
    url = "http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids=1.000001,0.399001&" \
          "fields=f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f64,f65,f70,f71,f76,f77,f82,f83,f164,f166,f168,f170,f172,f252,f253,f254,f255,f256,f124,f6,f278,f279,f280,f281,f282&" \
          "ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery18303224400345741254_1596166834140&_={}".format(
        round(time.time() * 1000))
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        if response.content.decode():
            response_str = response.content.decode().split('(')[1].replace(')', '').replace(';', '')
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


# -----------------------------------------------------------------------------------------------------------
def get_ShareHolding(type='SZ', start=None, end=None):
    start = str(start)[:10]
    end = str(end)[:10]
    type = str(type)

    # url = "https://testhqapi.niuguwang.com/api/ShareHolding/{}ShareHolding?beginTime={}&endTime={}"\
    #     .format(type,start,end)
    url = "https://hqapi.niuguwang.com/api/ShareHolding/{}ShareHolding?beginTime={}&endTime={}" \
        .format(type, start, end)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        if response.content.decode():
            response_json = json.loads(response.content.decode())
            if response_json['code'] == 0:
                data = response_json['data']['list']
                df_data = pd.DataFrame(data)
                return df_data
                # date_list = df_data['shareHoldingDate'].tolist()
                # new_date_list = [str(datetime.datetime.strptime(str(i), '%Y-%m-%dT%H:%M:%S'))[:19] for i in date_list]
                # df_data['shareHoldingDate'] = new_date_list
                # return df_data
            else:
                return None
        else:
            return None


def get_HKTradeCalendar(start=None, end=None):
    start = str(start)[:10]
    end = str(end)[:10]

    # url = "https://testhqapi.niuguwang.com/api/HKTradeCalendar?beginDate={}&endDate={}".format(start,end)
    url = "https://hqapi.niuguwang.com/api/HKTradeCalendar?beginDate={}&endDate={}".format(start, end)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        if response.content.decode():
            response_json = json.loads(response.content.decode())
            if response_json['code'] == 0:
                data = response_json['data']
                df_data = pd.DataFrame(data)
                return df_data
            else:
                return None
        else:
            return None


# ----------------------------------------------------------------------------------------------------------------------
def get_north_capital(start_date=None, end_date=None):
    sql_info = {
        'host': MYSQL_2_HOST,
        'port': MYSQL_2_PORT,
        'database': MYSQL_2_DATABASE,
        'user': MYSQL_2_USER,
        'password': MYSQL_2_PASSWORD,
    }
    start_date = str(start_date)[:10]
    end_date = str(end_date)[:10]
    try:
        sql = """select Buy,Sale,BuyAndSale,BuyAndSaleAddUp,TypeVal,SourceVal,Date
         from north_capital_history where Date>='{}' and Date<='{}' order by Date;""".format(start_date, end_date)
        # print(sql)
        data = conn_mysql_select(sql, sql_info)
        if data:
            df_data = pd.DataFrame(data)
            df_data.columns = ['Buy', 'Sale', 'BuyAndSale', 'BuyAndSaleAddUp', 'TypeVal', 'SourceVal', 'Date']
            return df_data
    except Exception:
        print(traceback.format_exc())


def get_north_top10(start_date=None, end_date=None):
    sql_info = {
        'host': MYSQL_2_HOST,
        'port': MYSQL_2_PORT,
        'database': MYSQL_2_DATABASE,
        'user': MYSQL_2_USER,
        'password': MYSQL_2_PASSWORD,
    }
    start_date = str(start_date)[:10]
    end_date = str(end_date)[:10]
    try:
        # sql = """select StockCode,Rank,ShortName,Buy,Sale,BuyAndSale,BuyAddSale,TypeVal,SourceVal,Date
        # from top10_trading_stocks where Date>='{}' and Date<='{}' order by Date;""".format(start_date,end_date)
        sql = """select *
        from top10_trading_stocks where TypeVal in (1,2) and Date>='{}' and Date<='{}' order by Date;""".format(start_date, end_date)
        # print(sql)
        data = conn_mysql_select(sql, sql_info)
        if data:
            df_data = pd.DataFrame(data)
            df_data.columns = ['Id', 'Rank', 'StockCode', 'ShortName', 'Buy', 'Sale', 'BuyAndSale', 'BuyAddSale',
                               'TypeVal', 'SourceVal', 'Date']
            df_data.drop('Id', axis=1, inplace=True)
            return df_data
    except Exception:
        print(traceback.format_exc())


# ----------------------------------------------------------------------------------------------------------------------
def get_PlateInfo(type=None):
    # url = "https://testhqapi.niuguwang.com/api/HKTradeCalendar?beginDate={}&endDate={}".format(start,end)
    url = "https://stq.niuguwang.com/ft/plateInfo?plateType={}".format(type)
    # print(url)
    try:
        headers = {
            'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        if response.content.decode():
            response_json = json.loads(response.content.decode())
            if response_json['resultCode'] == 0:
                data = response_json['data']
                df_data = pd.DataFrame(data)
                df_data.columns = ['InnerCode', 'Name', 'PlateCode', 'PlateInnerCode', 'PlateName', 'Symbol']
                return df_data
            else:
                return None
        else:
            return None


# -------------------contract api---------------------------------------------------------------------------------------------------

def freq2dataType(freq=None):
    # print(freq)
    if freq is None:
        return 60
    elif freq == '10s':
        return 10
    elif freq == '1m':
        return 60
    elif freq == '5m':
        return 5 * 60
    elif freq == '15m':
        return 15 * 60
    elif freq == '30m':
        return 30 * 60
    elif freq == '60m':
        return 60 * 60
    elif freq == '1d':
        return 60 * 60 * 24
    elif freq == '1w':
        return 60 * 60 * 24 * 7
    else:
        return 60 * 60 * 24

def exchange2num(exchange):
    if exchange is None:
        return 4
    # 中金所
    elif exchange == 'CFFEX':
        return 3
    # 上期所
    elif exchange == 'SHFE':
        return 4
    # 大商所
    elif exchange == 'DCE':
        return 5
    # 郑商所
    elif exchange == 'CZCE':
        return 6
    # 上海国际能源交易中心
    elif exchange == 'INE':
        return 15



def get_hisBar_raw(symbol=None, exchange=None, freq=None, start=None, end=None, count=None):
    # body = {"symbol": "rb2010", "exchange": 4, "dataType": 60, "begin": "20201009", "end": "20201020"}
    exchange_ = exchange2num(exchange)
    dataType = freq2dataType(freq=freq)

    url = ''
    body = {"symbol": symbol, "exchange": exchange_, "dataType": dataType, "dataSource":1}
    if start and end and not count:
        begin = start.replace('-', '').replace(' ', '').replace(':', '')
        end = end.replace('-', '').replace(' ', '').replace(':', '')
        body['begin'] = begin
        body['end'] = end
        url = "https://apigateway.inquantstudio.com/api/MarketData/GetHisBar"
    if not start and not end and count:
        body['count'] = count
        url = "https://apigateway.inquantstudio.com/api/MarketData/GetLastBar"
    if not start and end and count:
        end = end.replace('-', '').replace(' ', '').replace(':', '')
        body['end'] = end
        body['count'] = count
        url = "https://apigateway.inquantstudio.com/api/MarketData/GetPreviousBar"
    # print(body)
    # print(url)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        df_data.columns = ['symbol', 'exchange', 'bar_type', 'time', 'pre_close', 'open', 'high', 'low', 'close',
                           'volume',
                           'turnover', 'open_interest', 'settlement']

        df_data_ = df_data.sort_values(by='time').reset_index(drop=True)
        return df_data_


def get_hisBar(symbol=None, exchange=None, freq=None, start=None, end=None, count=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_hisBar_raw(symbol=symbol, exchange=exchange, freq=freq, start=start, end=end, count=count)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue


# ----------------------------------------------------------------------------------------------------------------------
def get_hisTick_raw(symbol=None, exchange=None, start=None, end=None, count=None):
    exchange_ = exchange2num(exchange)

    url = ''
    body = {"symbol": symbol, "exchange": exchange_, "dataSource":1}
    if start and end and not count:
        begin = start.replace('-', '').replace(' ', '').replace(':', '')
        end = end.replace('-', '').replace(' ', '').replace(':', '')
        body['begin'] = begin
        body['end'] = end
        url = "https://apigateway.inquantstudio.com/api/MarketData/GetHisTick"
    if not start and not end and count:
        body['count'] = count
        url = "https://apigateway.inquantstudio.com/api/MarketData/GetLastTick"
    if not start and end and count:
        end = end.replace('-', '').replace(' ', '').replace(':', '')
        body['end'] = end
        body['count'] = count
        url = "https://apigateway.inquantstudio.com/api/MarketData/GetPreviousTick"

    # print(body)
    # print(url)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        # print(df_data)
        df_data.columns = ['symbol', 'exchange', 'time',
                           'last', 'open', 'high', 'low', 'pre_close',
                           'volume','turnover',
                           'bid','ask','upper_limit','lower_limit',
                           'open_interest', 'settlement']
        return df_data


def get_hisTick(symbol=None, exchange=None, start=None, end=None, count=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_hisTick_raw(symbol=symbol, exchange=exchange, start=start, end=end, count=count)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue


# ----------------------------------------------------------------------------------------------------------------------
# 获取某一时刻的全部价格
def all_contract_price_raw(freq=None, time=None):
    dataType = freq2dataType(freq=freq)
    body = {"dataType": dataType}
    if time:
        time_ = time.replace('-', '').replace(' ', '').replace(':', '')
        if freq == '1d':
            time_ = time_[:8]+'000000'
        body['time'] = time_
    else:
        pass
    url = "https://apigateway.inquantstudio.com/api/MarketData/GetBarsByTime"
    # print(body)
    # print(url)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        # print(df_data)
        df_data.columns = ['symbol', 'exchange', 'bar_type', 'time', 'pre_close', 'open', 'high', 'low', 'close',
                           'volume',
                           'turnover', 'open_interest', 'settlement']
        return df_data


def all_contract_price(freq=None, time=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = all_contract_price_raw(freq=freq, time=time)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue
# ----------------------------------------------------------------------------------------------------------------------


def contract_depth_raw(symbol=None, exchange=None):
    exchange_ = exchange2num(exchange)

    body = {"symbol": symbol, "exchange": exchange_, "dataType": 1, "count": 1}
    # print(body)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://apigateway.inquantstudio.com/api/MarketData/GetLastTick"
        # print(url)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')[0]
        # return data
        bid = [[i['p'],i['v']] for i in data['bid']]
        ask = [[i['p'],i['v']] for i in data['ask']]
        c_depth = {'bid':bid,'ask':ask,'time':str(datetime.datetime.strptime(str(data['t']),'%Y%m%d%H%M%S'))}
        return c_depth


def contract_depth(symbol=None, exchange=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = contract_depth_raw(symbol=symbol, exchange=exchange)
        if data:
            return data
        i += 1
        time.sleep(0.01)
        continue


# ----------------------------------------------------------------------------------------------------------------------
def contract_all_position_users_raw(code=None,start=None,end=None,sign=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        # url = 'https://dev-riskadmin.inquant.cn/api/position/GetSymbolDetail?startTime={}&endTime={}&sign={}'.format(start,end,sign)
        url = "https://riskadmin.inquant.cn/api/position/GetRiskContractByCode?startTime={}&endTime={}&code={}&sign={}".format(start,end,code,sign)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        # print(response_json)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def contract_all_position_users(code=None,start=None,end=None,sign=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = contract_all_position_users_raw(code=code,start=start,end=end,sign=sign)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue


# def contract_position_users_raw(start=None,end=None):
#     m = hashlib.md5()
#     m.update('inquantRisk:{}{}'.format(start,end).encode('utf-8'))
#     sign = m.hexdigest().upper()
#     # print(body)
#     try:
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
#             "Content-Type": "application/json"}
#         # url = 'https://dev-riskadmin.inquant.cn/api/position/GetSymbolDetail?startTime={}&endTime={}&sign={}'.format(start,end,sign)
#         url = "https://riskadmin.inquant.cn/api/position/GetSymbolDetail?startTime={}&endTime={}&sign={}".format(start,end,sign)
#         # print(url)
#         response = requests.get(url, headers=headers)
#         response.close()
#     except Exception:
#         print(traceback.format_exc())
#         return None
#     else:
#         response = response.content.decode()
#         response_json = json.loads(response)
#         # print(response_json)
#         data = response_json.get('data')
#         df_data = pd.DataFrame(data)
#         return df_data
#
#
# def contract_position_users(start=None,end=None):
#     delay_times = 5
#     i = 0
#     while i < delay_times:
#         data = contract_position_users_raw(start=start,end=end)
#         if isinstance(data, pd.DataFrame):
#             if not data.empty:
#                 return data
#         i += 1
#         time.sleep(0.01)
#         continue


def contract_position_users_raw(start=None,end=None,sign=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        # url = 'https://dev-riskadmin.inquant.cn/api/position/GetSymbolDetail?startTime={}&endTime={}&sign={}'.format(start,end,sign)
        url = "https://riskadmin.inquant.cn/api/position/GetSymbolDetail?startTime={}&endTime={}&sign={}".format(start,end,sign)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        # print(response_json)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def contract_position_users(start=None,end=None,sign=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = contract_position_users_raw(start=start,end=end,sign=sign)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue



def get_spot_price_raw(spotCode=None,start=None,end=None):
    m = hashlib.md5()
    m.update('inquantSpotContract:{}{}{}'.format(spotCode,start,end).encode('utf-8'))
    sign = m.hexdigest().upper()
    # print(body)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://hq.inquant.cn/newsfut/api/spotcontract/getspothisprice?startTime={}&endTime={}&spotCode={}&sign={}"\
            .format(start,end,spotCode,sign)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        # print(response_json)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_spot_price(spotCode=None,start=None,end=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_spot_price_raw(spotCode=spotCode,start=start,end=end)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue




def get_all_spot_raw():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://hq.inquant.cn/newsfut/api/spotcontract/getallspotcontract"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        # print(response_json)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_all_spot():
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_all_spot_raw()
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue

# -----------------------------------------------------------------------------------------------------
# 获取所有合约
def get_all_contract_raw():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://apigateway.inquantstudio.com/api/BasicData/GetAllContract"
        # print(url)
        response = requests.post(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_all_contract():
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_all_contract_raw()
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue

# -----------------------------------------------------------------------------------------------------
# 获取所有合约分类
def get_contract_varieties_raw(type=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://hq.inquant.cn/hqfut/MktData/varietiesInfos.ashx?type={}".format(type)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        # print(response_json)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_contract_varieties(type=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_contract_varieties_raw(type=type)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue


def get_TradeVolumeRanking_raw(vid=None,start=None,end=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://hq.inquant.cn/info/positiondata/GetTradeVolumeRankingByVid?vid={}&startTime={}&endTime={}"\
            .format(vid,start,end)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        # print(response_json)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_TradeVolumeRanking(vid=None,start=None,end=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_TradeVolumeRanking_raw(vid=vid,start=start,end=end)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue



# -----------------------------------------------------------------------------------------------------

# 获取单个合约
def get_contract_detail_raw(symbol=None, exchange=None):
    # body = {"symbol": "rb2010", "exchange": 4}
    exchange_ = exchange2num(exchange)

    body = {"symbol": symbol, "exchange": exchange_}
    # print(body)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://apigateway.inquantstudio.com/api/BasicData/GetContract"
        # print(url)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        return data


def get_contract_detail(symbol=None,exchange=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_contract_detail_raw(symbol=symbol, exchange=exchange)
        if data:
            return data
        i += 1
        time.sleep(0.01)
        continue




# 获取所有合约
def get_contract_openTime_raw(start=None,end=None):
    start_ = start.replace('-','') + '000000'
    end_ = end.replace('-','') + '000000'
    body = {"begin": start_, "end": end_}
    # print(body)
    print(json.dumps(body))
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://apigateway.inquantstudio.com/api/BasicData/GetOpenTimes"
        print(url)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_contract_openTime(start=None,end=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_contract_openTime_raw(start=start,end=end)
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue



# 获取单个合约
def get_main_contract_raw(variety_code=None):
    body = {"varietyCode": variety_code}
    # print(body)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "https://apigateway.inquantstudio.com/api/BasicData/GetMainContract"
        # print(url)
        response = requests.post(url, data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        return data


def get_main_contract(variety_code=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_main_contract_raw(variety_code=variety_code)
        if data:
            return data
        i += 1
        time.sleep(0.01)
        continue

# ----------------------------------------------------------------------------------------------------------------------

# 获取期货手续费率



# 获取乘数、保证金比率
def get_all_commission_raw():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/GetAllExchFares"
        # url = "http://dev-taojinairobot.inquant.cn/Trade/GetAllExchBails"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_all_commission():
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_all_commission_raw()
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue



# 获取乘数、保证金比率
def get_all_margin_ratios_raw():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/GetAllExchBails"
        # url = "http://dev-taojinairobot.inquant.cn/Trade/GetAllExchBails"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_all_margin_ratios():
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_all_margin_ratios_raw()
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue



# 获取所有品种variety
def get_all_varieties_raw():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/GetAllVarietys"
        # url = "http://dev-taojinairobot.inquant.cn/Trade/GetAllVarietys"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_all_varieties():
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_all_varieties_raw()
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue



# ----------------------------------------------------------------------------------
# 获取所有 机器人id
def get_all_robots_info_raw():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/AiRobot/GetAllAvailableAiRobots"
        # url = "http://dev-taojinairobot.inquant.cn/AiRobot/GetAllAvailableAiRobots"
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        data = response_json.get('data')
        df_data = pd.DataFrame(data)
        return df_data


def get_all_robots_info():
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_all_robots_info_raw()
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                return data
        i += 1
        time.sleep(0.01)
        continue



# 获取 某个机器人信息
def get_robot_info_raw(robotId=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/AiRobot/GetAiRobotInfo?robotId={}".format(robotId)
        # url = "http://dev-taojinairobot.inquant.cn/AiRobot/GetAiRobotInfo?robotId={}".format(robotId)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        # print(response_json)
        data = response_json.get('data')
        return data


def get_robot_info(robotId=None):
    delay_times = 5
    i = 0
    while i < delay_times:
        data = get_robot_info_raw(robotId=robotId)
        if data:
            return data
        i += 1
        time.sleep(0.01)
        continue



# http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/GetStgyAccountInfo?stgyAccountId=1
# http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/GetStgyAccountInfo?stgyAccountId=1
# 获取 某个账户的机器人信息
def get_account_info(stgyAccountId=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/GetStgAccontInfo?stgyAccountId={}".format(stgyAccountId)
        # url = "http://dev-taojinairobot.inquant.cn/Trade/GetStgyAccountInfo?stgyAccountId={}".format(stgyAccountId)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        return response_json

#



# 获取机器人上一天的equity
def get_RobotLastEquity(robotId=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/AiRobot/GetPreAsset?robotId={}".format(robotId)
        # url = "http://dev-taojinairobot.inquant.cn/AiRobot/GetPreAsset?robotId={}".format(robotId)

        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        return response_json['data']




# 获取 某个机器人持仓
def get_robot_position(stgyAccount=None,symbol_exchange=None,posSide=None):
    symbol = symbol_exchange.split('.')[0]
    exchange = symbol_exchange.split('.')[1]
    exchange_num = exchange2num(exchange)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/GetPosition?stgyAccount={}&symbol={}&exchange={}&posSide={}"\
            .format(stgyAccount, symbol,exchange, posSide)
        # url = "http://dev-taojinairobot.inquant.cn/Trade/GetPosition?stgyAccount={}&symbol={}&exchange={}&posSide={}"\
        #     .format(stgyAccount, symbol,exchange_num, posSide)
        # url = "http://dev-taojinairobot.inquant.cn/AiRobot/GetAiRobotInfo?robotId={}".format(robotId)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        # print(response_json)
        # data = response_json.get('data')
        return response_json



# 停止 某个机器人
def stop_robot(robotId=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/AiRobot/StopAiRobot?robotId={}".format(robotId)
        # url = "http://dev-taojinairobot.inquant.cn/AiRobot/StopAiRobot?robotId={}".format(robotId)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        return response_json


# ----------------------------------------------------------------------------------
# 策略信号新增
def SendStrategySignal(stgyId=None,symbol=None,exchange=None,side=None,quantity=None,price=None,
                       orderType=None,note=None):
    exchange_num = exchange2num(exchange)
    side_offset = {'open_long':[66,1],'close_long':[66,2],'open_short':[83,1],'close_short':[83,2]}
    side_, offset = side_offset[side]
    body = {
        "stgyId": stgyId,
        "symbol": symbol,
        "exchange": exchange_num,
        "orderSide": side_,
        "offset": offset,
        "quantity": quantity,
        "price": price,
        "orderType": 1,
        "note": note,
    }
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/SendStgySignal"
        # url = "http://dev-taojinairobot.inquant.cn/Trade/SendStgySignal"
        # print(url)
        response = requests.post(url,data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        return response_json



# 获取策略订单信息(策略订单的状态)
def OmsContract_GetOrderStatus(stgyOrderId=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/QryStgyOrderStatus?stgyOrderId={}".format(stgyOrderId)
        # url = "http://dev-taojinairobot.inquant.cn/Trade/QryStgyOrderStatus?stgyOrderId={}".format(stgyOrderId)
        # print(url)
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        return response_json


# 下单
def OmsContract_CreateOrder(stgyAccountId=None,stgySignalId=None,symbol_exchange=None,side=None,quantity=None,is_today=None):
    symbol = symbol_exchange.split('.')[0]
    exchange = symbol_exchange.split('.')[1]
    exchange_num = exchange2num(exchange)
    # 平今 3
    if is_today:
        if exchange_num == 4:
            side_offset = {'open_long': [66, 1], 'close_long': [83, 3], 'open_short': [83, 1], 'close_short': [66, 3]}
        else:
            side_offset = {'open_long': [66, 1], 'close_long': [83, 2], 'open_short': [83, 1], 'close_short': [66, 2]}
    # 平昨 2
    else:
        if exchange_num == 4:
            side_offset = {'open_long':[66,1],'close_long':[83,2],'open_short':[83,1],'close_short':[66,2]}
        else:
            side_offset = {'open_long': [66, 1], 'close_long': [83, 2], 'open_short': [83, 1], 'close_short': [66, 2]}
    side_, offset = side_offset[side]
    body = {
        "stgyAccountId": stgyAccountId,
        "stgySignalId": stgySignalId,
        "symbol": symbol,
        "exchange": exchange_num,
        "orderSide": side_,
        "offset": offset,
        "quantity": quantity,
        "price": 1,
        "orderType": 1}

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/SendOrder"
        # url = "http://dev-taojinairobot.inquant.cn/Trade/SendOrder"
        # print(url)
        response = requests.post(url,data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        return response_json



# 撤单
def OmsContract_CancelOrder(stgyOrderId=None,stgyAccountId=None):
    body = {
        "stgyOrderId": stgyOrderId,
        "stgyAccountId": stgyAccountId
    }
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
            "Content-Type": "application/json"}
        url = "http://iqfairobotwebapi.taojin.svc.ingress.inquant/Trade/CancelOrder"
        # url = "http://dev-taojinairobot.inquant.cn/Trade/CancelOrder"
        # print(url)
        response = requests.post(url,data=json.dumps(body), headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
        return None
    else:
        response = response.content.decode()
        response_json = json.loads(response)
        return response_json

















# -----------------------------------------------------------------------------------------------
def get_AllOTCFundsInfo():
    # url = "http://127.0.0.1:5007/funds/info"
    url = "https://stq.niuguwang.com/funds/info"
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        if not response_json['data']:
            return pd.DataFrame()
        return pd.DataFrame(response_json['data'])
    except Exception:
        print(traceback.format_exc())

def get_OTCFundsValues(code=None,start=None,end=None):
    # url = 'https://shqf.niuguwang.com/fquote/OPF/nopfquotedata.ashx?code={}&ntype=2'.format(innercode)
    # # print(url)
    # try:
    #     headers = {"Content-Type": "application/json",
    #                'User-Agent':get_ua()}
    #     response = requests.get(url, headers=headers).content.decode()
    #     response_json = json.loads(response)
    #     data_dict = response_json.get('timedata')
    #     if data_dict:
    #         df_data = pd.DataFrame(response_json['timedata'])
    #         return df_data[['date','value','value1','value2','updownrate','updownrate1','updownrate2']]
    #     else:
    #         return pd.DataFrame()
    # except Exception:
    #     print(traceback.format_exc())

    url = 'https://stq.niuguwang.com/funds/values?code={}&start={}&end={}'.format(code,start,end)
    # print(url)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        data_dict = response_json.get('data')
        if data_dict:
            df_data = pd.DataFrame(response_json['data'])
            return df_data[['Date','FundCode','PerNetValue','TotalNetValue','RiseRate','ShenGouStatus','ShuHuiStatus']]
        else:
            return pd.DataFrame()
    except Exception:
        print(traceback.format_exc())


def get_OTCFundsInfo(innercode=None):
    url = 'https://shqf.niuguwang.com/fquote/OPF/nopfquotedata.ashx?code={}&ntype=2'.format(innercode)
    # print(url)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        data_dict = response_json.get('timedata')
        if data_dict:
            del response_json['timedata']
            return response_json
        else:
            return response_json
    except Exception:
        print(traceback.format_exc())



def get_OPF_PORTFOLIO(code=None):
    url = 'https://stq.niuguwang.com/funds/portfolio?code={}'.format(code)
    # print(url)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        if not response_json['data']:
            return pd.DataFrame()
        df_data = pd.DataFrame(response_json['data'])
        return df_data
    except Exception:
        print(traceback.format_exc())



def get_OPF_AssetConfig(code=None):
    url = 'https://stq.niuguwang.com/funds/AssetConfig?code={}'.format(code)
    # print(url)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        if not response_json['data']:
            return pd.DataFrame()
        df_data = pd.DataFrame(response_json['data'])
        return df_data
    except Exception:
        print(traceback.format_exc())



def get_OPF_AssetConfig_Exe(code=None):
    url = 'https://stq.niuguwang.com/funds/AssetConfig_Exe?code={}'.format(code)
    # print(url)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        if not response_json['data']:
            return pd.DataFrame()
        df_data = pd.DataFrame(response_json['data'])
        return df_data
    except Exception:
        print(traceback.format_exc())

def get_OPF_Bouns(code=None):
    url = 'https://stq.niuguwang.com/funds/Bonus?code={}'.format(code)
    # print(url)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        if not response_json['data']:
            return pd.DataFrame()
        df_data = pd.DataFrame(response_json['data'])
        return df_data[['FundCode','DengJiDate','ChuXiDate','FaFangDate','Bonus','AddTime']]\
            .sort_values(by=["ChuXiDate"],ascending=[False])
    except Exception:
        print(traceback.format_exc())
# -----------------------------------------------------------------------------------------------





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

    # end_date = str(datetime.datetime.now())[:10]
    # data = get_stock_data(code='000529.SZ', freq='d', bars=2, end=end_date)
    # print(data)
    # value = round(float(data.iloc[-1]['close']), 4)  # open_price
    # print(value)
    # data = get_turnOver(inner_list=[1,2,3,4])
    # print(data)

    t1 = time.time()
    # df = get_allStock()
    # print(df)
    # innercode = df[df['code'] == '600299.SH']
    # print(innercode)

    # try:
    #     innercode = int(df[df['code'] == '600299.SH']['innercode'].tolist()[0])
    #     name = str(df[df['code'] == '002075.SZ']['name'].tolist()[0])
    # except:
    #     innercode = -1
    #     name = '无敌旋风'
    #
    # print(innercode)
    # print(name)

    # data = get_ShareHolding(type='SZ', start='2020-09-01', end='2020-09-28')
    # print(data)
    # data = get_ShareHolding(type='SH',start='2020-09-01', end='2020-09-28')
    # print(data)
    # data = get_ShareHolding(type='HKSHSZ', start='2020-09-01', end='2020-09-28')
    # print(data)
    #
    # data = get_HKTradeCalendar(start='2020-09-01', end='2020-09-28')
    # print(data)

    # data = get_PlateInfo(type=1)
    # print(data)

    data = get_depth(code='000001.SZ')
    print(data)




    print(time.time() - t1)

    # print(time.time()-start_)
