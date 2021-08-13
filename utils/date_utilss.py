__author__ = 'wangjian'
import datetime
import time
import ngwshare as ng
import pandas as pd


def getTradingCalendar(start=None,end=None):
    if not start:
        start = '2018-01-01'
    if not end:
        end = '2023-01-01'
    body = {
        "table": 'QT_TradingDayNew',
        "field_list": ['TradingDate', 'IfTradingDay', 'SecuMarket'],
        "alterField": 'TradingDate',
        "startDate": start,
        "endDate": end
    }
    data = ng.get_fromDate(body)
    return data


def is_trading_day(date=None,data=pd.DataFrame()):
    date = str(date)[:10]+' 00:00:00'
    if data.empty:
        body = {
                "table": 'QT_TradingDayNew',
                "field_list": ['TradingDate', 'IfTradingDay', 'SecuMarket'],
                "alterField": 'TradingDate',
                "startDate": '2018-01-01',
                "endDate": '2023-01-01'
        }
        data = ng.get_fromDate(body)
    data = data.loc[data.SecuMarket==83].drop('SecuMarket',axis=1)
    # print(data)
    flag = data.loc[data.TradingDate==date].IfTradingDay.values[0]
    if flag == 1:
        return True
    else:
        return False


def return_last_trading_day(date=None,data=pd.DataFrame()):
    if date:
        if isinstance(date,str):
            if len(date) == 10:
                now_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            elif len(date) == 19:
                now_date =  datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            else:
                now_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
        elif isinstance(date, datetime.date):
            now_date = date
        else:
            now_date = datetime.datetime.now()
    else:
        now_date = datetime.datetime.now()
    if data.empty:
        body = {
                "table": 'QT_TradingDayNew',
                "field_list": ['TradingDate', 'IfTradingDay', 'SecuMarket'],
                "alterField": 'TradingDate',
                "startDate": '2018-01-01',
                "endDate": '2023-01-01'
        }
        data = ng.get_fromDate(body)
    data = data.loc[data.SecuMarket==83].drop('SecuMarket',axis=1)
    while True:
            l_date = now_date - datetime.timedelta(days=1)
            l_date = str(l_date)[:10] + ' 00:00:00'
            l_flag = data.loc[data.TradingDate == l_date].IfTradingDay.values[0]
            if l_flag == 1:
                return str(l_date)[:10]
            else:
                now_date = datetime.datetime.strptime(l_date, '%Y-%m-%d %H:%M:%S')
                continue


def return_next_trading_day(date=None, data=pd.DataFrame()):
    if date:
        if isinstance(date,str):
            if len(date) == 10:
                now_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            elif len(date) == 19:
                now_date =  datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            else:
                now_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
        elif isinstance(date, datetime.date):
            now_date = date
        else:
            now_date = datetime.datetime.now()
    else:
        now_date = datetime.datetime.now()

    if data.empty:
        body = {
                "table": 'QT_TradingDayNew',
                "field_list": ['TradingDate', 'IfTradingDay', 'SecuMarket'],
                "alterField": 'TradingDate',
                "startDate": '2018-01-01',
                "endDate": '2023-01-01'
        }
        data = ng.get_fromDate(body)
    data = data.loc[data.SecuMarket==83].drop('SecuMarket',axis=1)

    while True:
            l_date = now_date + datetime.timedelta(days=1)
            l_date = str(l_date)[:10] + ' 00:00:00'
            l_flag = data.loc[data.TradingDate == l_date].IfTradingDay.values[0]
            if l_flag == 1:
                return str(l_date)[:10]
            else:
                now_date = datetime.datetime.strptime(l_date, '%Y-%m-%d %H:%M:%S')
                continue


if __name__ == '__main__':
    data = getTradingCalendar()
    print(data)

    aa = is_trading_day('2020-10-09',data)
    print(aa)

    aa = is_trading_day('2020-10-01',data)
    print(aa)

    t1111 = time.time()


    da = return_last_trading_day('2020-09-30',data)
    print(da)

    da = return_last_trading_day(data=data)
    print(da)



    print(time.time()-t1111)


    da = return_next_trading_day('2020-10-09',data)
    print(da)

    da = return_next_trading_day(data=data)
    print(da)
