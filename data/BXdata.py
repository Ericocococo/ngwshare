import requests
import json
import pandas as pd
import time
import urllib3
from datetime import datetime
from chinese_calendar import is_holiday
import datetime
from ngwshare.utils.http_util import get_ua


def day_offset(nums, ndate):
    today = datetime.datetime.strptime(ndate, "%Y-%m-%d").date()  # 将字符串日期转换为datetime格式的日期
    count = 0
    tom_date = today
    one = datetime.timedelta(days=1)
    while count < abs(nums):
        #往后延一日后的时间
        tom_date = tom_date + one if nums > 0 else tom_date - one
        d_wd = tom_date.weekday() + 1
        if is_holiday(tom_date) or d_wd == 6 or d_wd == 7:
            continue
        count += 1
    return datetime.datetime.strftime(tom_date, "%Y-%m-%d")

def day_filter(startDate,endDate):
    hol_day = []
    tra_day = []
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    # 中国的节假日日期数组
    while startDate <= endDate:
        if is_holiday(startDate) or startDate.weekday() == 6 or startDate.weekday() == 7:
            hol_day.append(datetime.datetime.strftime(startDate, "%Y-%m-%d"))  # 节假日+1
        else:
            tra_day.append(datetime.datetime.strftime(startDate, "%Y-%m-%d"))
        startDate += datetime.timedelta(days=1)
    # 返回工作日
    return len(tra_day)


def get_north_jg(sdate, edate):
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/data"
    days = day_filter(sdate, edate)
    # print(days)
    if days >= 20:
        raise Exception("超出查询时间区间，限制日期区间内交易日天数为20日")
    parms = {
        'sdate': sdate,  # 发送给服务器的内容
        'edate': edate
    }
    # headers = {
    #     'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    #     'Spam': 'Eggs',
    #     'Connection': 'close'
    # }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=parms, headers=headers, verify=False, timeout=60)  # 发送请求
    text = res.text
    dict = json.loads(text)
    df = pd.DataFrame(dict)
    # e = time.time()
    # print(e-s)
    return df

def get_free_value(ticker, sdate, edate):
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/freevalue"
    # url = "http://127.0.0.1:5000/NorthJg/GetNorthJg/ho"
    # url = "http://dev-www.test.niuguwang/NorthJg/GetNorthJg/freevalue"
    parms = {
        'sdate': sdate,  # 发送给服务器的内容
        'edate': edate,
        'ticker': str(ticker)
    }
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    urllib3.disable_warnings()
    res = requests.post(url, data=parms, headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    # print(text)
    dict = json.loads(text)
    df = pd.DataFrame(dict)
    return df




def get_weight_date(index_code, sdate, edate):
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/hsweight"
    # url = "http://127.0.0.1:5000/NorthJg/GetNorthJg/freevalue"
    # url = "http://dev-www.test.niuguwang/NorthJg/GetNorthJg/hsweight"
    parms = {
        'sdate': sdate,  # 发送给服务器的内容
        'edate': edate,
        'index_code': index_code
    }
    # print(parms)
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Spam': 'Eggs',
        'Connection': 'close'
    }
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=parms, headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)
    df = pd.DataFrame(dict)
    return df


if __name__ == '__main__':
    t1 = time.time()

    # data = get_north_jg("2020-08-17", "2020-08-19")
    # print(data)

    # data = get_free_value('002615.SZ', "2015-03-09", "2015-03-14")
    # print(data)

    # HS300个股权重
    data = get_weight_date("000300.SH", "2021-06-11", "2021-06-11")
    print(data)


    print(time.time()-t1)


