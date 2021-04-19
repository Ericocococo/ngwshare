import datetime
import ngwshare as ng
import time
import pandas as pd
# pd.set_option('display.height',1000)
from ngwshare.utils.date_util import str2datetime

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)





# # # 获取K线
# df = ng.get_k_data(code='000058.SH',freq='d',start='2020-01-01',end='2020-05-15')
# print(df)
#
# df = ng.get_k_data(code='001914.SZ', freq='d',start='2019-01-01', end='2020-07-01')
# print(df)



# df = ng.get_k_data(code='000058.SH',freq='d',enfd='2020-05-15',bars=30)
# print(df)
#
#
#
#
# # 获取股票基本信息
# df = ng.get_stock_basic(code='000058.SH')
# print(df)

# 000760.SZ
# # 获取所有股票代码
# df = ng.get_all_stock()
# print(df['code'].tolist())
# print(len(df['code'].tolist()))


#
# 总市值、流通市值等
# df = ng.get_performance('2020-05-25')
# print(df)

#
# # 市盈率、市净率等(加入InsertTime)
# df = ng.get_dIndicesForValuation('2020-05-25')
# print(df)
#
# # 研报
# df = ng.get_c_RR_ResearchReport(name='国泰君安', start='2020-05-10', end='2020-05-12')
# print(df)
#
# # ST
# df = ng.get_specialTrade()
# print(df)
#
#
# # 陆股通
# df = ng.hk_hold('20190625')
# print(df)



# # 根据表，字段 获取财务数据
# table = 'LC_MainQuarterData'
# stock_tuple = ['000007.SZ','600722.SH','000501.SZ']
# filed_list = ['EndDate','BasicEPS','DilutedEPS']
# start = '2010-01-01'
# end = '2020-05-15'
# data = ng.get_financialData(table, stock_tuple, filed_list, start, end)
# print(data)
#
#
# table = 'LC_MainDataNew'
# stock_tuple = ['600064.SH']
# filed_list = ['BasicEPS']
# start = '2010-01-01'
# end = '2020-05-15'
# data = ng.get_financialData(table, stock_tuple, filed_list, start, end)
# print(data)


# table = 'LC_MainDataNew'
# stock_tuple = ['300033.SZ']
# filed_list = ['InfoPublDate','EndDate','NetProfit','BulletinType','BulletinType']
# start = '2018-05-15'
# end = '2020-04-15'
# df = ng.get_financialData(table, stock_tuple, filed_list, start, end)
# print(df)


# 通过指定表 指定日期类型字段 筛选
# table = 'LC_NewestFinaIndex'
# alterField = 'AdjustDate'
# filed_list = ['ShareCapitalAftereAdjust','RetainedProfitBeforeAdjust','EPS']
# start = '2020-01-15'
# end = '2020-05-15'
# df = ng.get_financialDataPro(table, alterField, filed_list, start, end)
# print(df)




# # 根据companyCode 查询表
# table = 'LC_NewestFinaIndex'
# alterField = 'AdjustDate'
# filed_list = ['EPS','EPSTTM']
# start = '2020-01-15'
# end = '2020-05-15'
# df = ng.get_fromCompany(table, alterField, filed_list, start, end)
# print(df)



# code_list = ["000858.SZ", "600722.SH", "000895.SZ", "600006.SH"]
# table = 'QT_DailyQuote'
# field_list = ["TradingDay", "PrevClosePrice", "OpenPrice", "HighPrice", "LowPrice"]
# body = {
#     "table": table,
#     "code_list": code_list,
#     # "all_code": True,
#     "field_list": field_list,
#     "alterField": "TradingDay",
#     # "alterField": "EndDate",
#     "startDate": "2018-05-23",
#     "endDate": "2020-05-26"
# }
# data = ng.get_fromCode(body)
# print(data)






# select InnerCode,
# RightRegDate, -- 股权登记日
# ExDiviDate, -- 除权除息日
# BonusShareListDate,-- 股息到帐日期/红利发放日
# ToAccountDate, -- 最后交易日
#
# BonusShareRatio, -- 送股比例(10送X)
# TranAddShareRaio, -- 转增股比例(10转增X)
# CashDiviRMB, -- 派现(含税/人民币元)
# ActualCashDiviRMB, -- 	实派(税后/人民币元)
#
# BonusSHRatioAdjusted, -- 送股比例(10送X)(计算除权价用)
# TranAddRatioAdjusted, -- 转增比例(10转增X)(计算除权价用)
# CashDiviRMBAdjusted -- 	派现(含税10派X元)(计算除权价用)
# from LC_Dividend where RightRegDate>'2020-01-01';


#
# t1 = time.time()
#
# code_list = ["000403.SZ", "300765.SZ", "600340.SH"]
# table = 'LC_Dividend'
# field_list = ["RightRegDate", "ExDiviDate", "BonusShareListDate", "ToAccountDate",
#               "BonusShareRatio","TranAddShareRaio","CashDiviRMB","ActualCashDiviRMB",
#               "BonusSHRatioAdjusted","TranAddRatioAdjusted","CashDiviRMBAdjusted"
#               ]
# body = {
#     "table": table,
#     "code_list": code_list,
#     # "all_code": True,
#     "field_list": field_list,
#     "alterField": "RightRegDate",
#     # "alterField": "EndDate",
#     "startDate": "1995-01-01",
#     "endDate": "2030-07-27"
# }
# data = ng.get_fromCode(body)
# print(data)
#
#
#
# print(time.time()-t1)




# body = {
#     "table": 'SecuMain',
#     "field_list": ['SecuCode', 'SecuAbbr', 'SecuMarket', 'ListedSector', 'ListedState'],
#     "alterFieldName": 'SecuCategory',
#     "name": [1],
# }
# dfgb_all_code = ng.get_fromName(body)
# print(dfgb_all_code)




# # company
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
# data = ng.get_fromCompany(body)
# print(data)
#
# # date
# table = 'QT_SHSZHSCTradingDay'
# field_list = ["EndDate", "TradingType", "IfWeekEnd", "IfYearEnd", "UpdateTime", "InfoSource"]
# body = {
#     "table": table,
#     "field_list": field_list,
#     "alterField": "EndDate",
#     "startDate": "2020-01-01",
#     "endDate": "2020-05-26"
# }
# data = ng.get_fromDate(body)
# print(data)






# table = 'NI_News_Industry'
# field_list = ['EventCode','EventEmotionCode','EventDate']
# filt_date = 'InsertTime'
# s_date = '2020-01-01'
# e_date = '2020-07-28'
#
# body = {
#     "table": table,
#     "field_list": field_list,
#     "alterField": filt_date,
#     "startDate": s_date,
#     "endDate": e_date,
# }
#
# df = ng.get_fromDate(body)
# print(df)



# table = 'LC_Dividend'
# field_list = ['EventCode','EventEmotionCode','EventDate']
# filt_date = 'InsertTime'
# s_date = '2020-01-01'
# e_date = '2020-07-28'
#
# body = {
#     "table": table,
#     "field_list": field_list,
#     "alterField": filt_date,
#     "startDate": s_date,
#     "endDate": e_date,
# }
#
# df = ng.get_fromDate(body)
# print(df)



# table = 'NI_News_Industry_SE'
# field_list = ['ID','TypeCode','Code']
#
# body = {
#     "table": table,
#     "field_list": field_list
# }
# df = ng.get_fromTable(body)
# print(df)
#
#
# table = 'CT_SystemConst'
# field_list = ['LB','DM','LBMC']
#
# body = {
#     "table": table,
#     "field_list": field_list
# }
# df = ng.get_fromTable(body)
# print(df)



# table = 'C_RR_ResearchReport'
# field_list = ["OrgName", "OrgNameDisc", "AreaCode", "Author", "WritingDate", "InsertTime"]
# name = ['国泰君安', '中信证券']
#
# body = {
#     "table": table,
#     "field_list": field_list,
#     "alterFieldName": "OrgNameDisc",
#     "name": name,
#     "alterFieldDate": "InfoPublDate",
#     "startDate": "2020-05-01",
#     "endDate": "2020-07-07"
# }
# data = ng.get_fromDateName(body=body)
# print(data)

# t1 = time.time()
#
#
# price = ng.get_price(codes=['000001.SZ', '600000.SH', '000028.SZ', "000858.SZ", "600722.SH", "000895.SZ", "600006.SH"])
# print(price)
#
#
# print(time.time()-t1)




# data = ng.get_stock_data(code='399006.SZ', freq='1m', adj='qfq', bars=300)
# print(data)

# data = ng.get_stock_data(code='399006.SZ', freq='5m', adj='qfq', bars=300)
# print(data)
# data = ng.get_stock_data(code='399006.SZ', freq='15m', adj='qfq', bars=300)
# print(data)
# data = ng.get_stock_data(code='399006.SZ', freq='30m', adj='qfq', bars=300)
# print(data)
# data = ng.get_stock_data(code='399006.SZ', freq='60m', adj='qfq', bars=300)
# print(data)

# data = ng.get_stock_data(code='399006.SZ', freq='w', adj='qfq', bars=50)
# print(data)
# data = ng.get_stock_data(code='399006.SZ', freq='mon', adj='qfq', bars=50)
# print(data)
#
#
# data = ng.get_stock_data(code='399006.SZ', freq='d', adj='qfq', bars=50)
# print(data)

# data = ng.get_stock_data(code='399006.SZ', freq='d', adj='qfq', start='2019-05-27', end='2020-08-27')
# print(data)

# data = ng.get_stock_data(code='000590.SZ', freq='d', adj='qfq', start='2020-08-26', end='2020-08-27')
# print(data)

# data = ng.get_stock_data(code='000590.SZ', freq='d', adj='qfq', bars=2)
# print(data)

#
# df = ng.get_allStock()
# print(df)


# df = ng.get_allStock()
# print(df)


# t11 = time.time()
#
# df = float(ng.get_k_data(code='000058.SZ',freq='d',end='2020-05-15',bars=1)['close'].tolist()[0])
# print(df)
#
# print(time.time()-t11)



# body = {
#     "table": 'SecuMain',
#     "field_list": ['SecuCode', 'SecuAbbr', 'SecuMarket', 'ListedSector', 'ListedState'],
#     "alterFieldName": 'SecuCategory',
#     "name": [1],
# }
# dfgb_all_code = ng.get_fromName(body)
# print(dfgb_all_code)
# df = ng.get_allStock()
# print(df)
# innerCode = df[df['code'] == '000058.SZ']['innercode'].tolist()[0]
# print(innerCode)
#
#
# print(time.time()-t11)


# t1 = time.time()
#
# data = ng.get_stock_data_inner_raw(innercode=661, freq='5m', adj='qfq', bars=400)
# print(data)
#
# print(time.time()-t1)
#
#
# t1 = time.time()
#
# data = ng.get_stock_data_inner(code='002153.SZ',innercode=661, freq='5m', adj='qfq', bars=400)
# # print(data)
#
# print(time.time()-t1)




# t1 = time.time()
#
# data = ng.get_stock_data_inner_raw(innercode=661, freq='d', adj='qfq', bars=400)
# print(data)
#
# print(time.time()-t1)
#
#
# t1 = time.time()
#
# data = ng.get_stock_data_inner(code='002153.SZ',innercode=661, freq='d', adj='qfq', bars=400)
# print(data)
#
# print(time.time()-t1)


# table = 'C_RR_ResearchReport_SE'
# field_list = ['ID', 'TypeCode', 'Code']
# body = {
#     "table": table,
#     "field_list": field_list,
#     "alterFieldName": 'ID',
#     "name": [649189259854, 649185930937, 649181845390, 649186813096, 649186754842]
# }
# df2 = ng.get_fromName(body)
# print(df2)





# df = ng.get_tick('002153.SZ')
# print(df)



# t1 = time.time()
#
# df = ng.get_trans(codes=['002153.SZ',1,'300856.SZ',12,'688580.SH'])
# print(df)

#
# print(time.time()-t1)



# t1 = time.time()

# df = ng.get_price(codes=['002153.SZ','300856.SZ','688580.SH'])
# print(df)


# print(time.time()-t1)


# while True:
#     a = ng.get_zjlx()
#     print(a, end='    ')
#     print(str(datetime.datetime.now())[:19])
#     time.sleep(1)





# data = ng.get_stock_data_inner(code='002437.SZ', innercode=945, freq='5m', adj='qfq', bars=300)
# print(data)

# data = ng.get_stock_data_inner(code='000001.SH', innercode=2318, freq='5m', adj='qfq', bars=300)
# print(data)




# data = ng.get_plate_data_inner(code='asdasd', innercode=2000018, freq='5m', adj='qfq', bars=300)
# print(data)
# # #
# # # a = data['date'].values[-1]
# # # print(a,type(a))
# #
# data = ng.get_plate_data_inner_raw(innercode=2000018, freq='5m', adj='qfq', bars=300)
# print(data)

# h = ng.get_stock_data(code="002705.SZ",  freq='30m', adj='qfq', end = '2020-08-31' ,bars=1000)
# print(h)

# h = ng.get_stock_data(code="600507.SH",  freq='d', adj='qfq', start='2015-01-01',end = '2016-08-31')
# print(h)


# h_raw = ng.get_stock_data(code='000001.SZ', innercode=1, freq='30m', adj='qfq', bars=300)
# print(h_raw)
# h_raw = ng.get_stock_data(code='000001.SZ', innercode=1, freq='5m', adj='qfq', bars=300)
# print(h_raw)
# h_raw = ng.get_stock_data(code='000001.SZ', innercode=1, freq='15m', adj='qfq', bars=300)
# print(h_raw)
# h_raw = ng.get_stock_data(code='000001.SZ', innercode=1, freq='60m', adj='qfq', bars=300)
# print(h_raw)
h_raw = ng.get_stock_data(code='000001.SZ', innercode=1, freq='1m', adj='qfq', bars=500)
print(h_raw)


# data = ng.get_stock_data(code='000029.SZ', freq='d', adj='qfq', end='2020-08-05',bars=300)
# print(data)


# stock_data = ng.get_allOnlyStock()
# print(stock_data)
#
# new_code = [str(i)[:6] for i in stock_data['code']]
#
# stock_data['code'] = new_code
# print(stock_data[['code','innercode','name','market']])



# ng.get_stock_data_inner(code='002437.SZ', innercode=945, freq='d', adj='qfq', bars=3)




# value = ng.get_depth('002534.SZ')
# print(value)

# aa = value['bids'][0][0]
# print(round(float(aa),4),type(aa))
#
# bb = value['asks'][0][0]
# print(round(float(bb),4),type(bb))
#
# if round(float(bb),4) == 0:
#     print('asdasd')



# innerlist=[1,2,3]
# data = ng.get_turnover(innerlist)
# print(data)






# a = ng.get_stock_data_inner(code='000300.SH',innercode=2131, freq='1m', bars=100)
# print(a)


# bm_value = ng.get_stock_data_inner(code='000300.SH',innercode=2131, freq='d', bars=1).close.values[-1]
# print(bm_value)



# ng.get_fromCode()
# ng.get_fromCompany()
# ng.get_fromDate()
#
# ng.get_fromDateName()
# ng.get_fromTable()
# ng.get_fromName()


# body = {
#         "table": 'QT_TradingDayNew',
#         "field_list": ['TradingDate', 'IfTradingDay', 'SecuMarket'],
#         "alterField": 'TradingDate',
#         "startDate": '2018-01-01',
#         "endDate": '2022-01-01'
# }
# data = ng.get_fromDate(body)
# print(data)




# body = {'table': 'C_EX_StockNetProfit',
#         'field_list': ['SecuCode','EndDate', 'StatisPeriod', 'StatisType', 'PNetProfitCount', 'PNetProfitAdd', 'PNetProfitReduce', 'ForecastYear'],
#         'startDate': '2020-09-17',
#         'endDate': '2020-09-17',
#         'alterFieldDate': 'EndDate',
#         'alterFieldName': 'StatisPeriod',
#         'name': [30]}
# data = ng.get_fromDateName(body)
# print(data)



# table = 'C_RR_ResearchReport'
# field_list = ["OrgName", "OrgNameDisc", "AreaCode", "Author", "WritingDate", "InsertTime"]
# # name = ['国泰君安']
# name = ['国泰君安', '中信证券']
#
# body = {
#     "table": table,
#     "field_list": field_list,
#     "alterFieldName": "OrgNameDisc",
#     "name": name,
#     "alterFieldDate": "InfoPublDate",
#     "startDate": "2020-05-01",
#     "endDate": "2020-07-07"
# }
# data = ng.get_fromDateName(body=body)
# print(data)



# bm_value = ng.get_k_data(code='000905.SH', freq='d', start='2020-09-23', end='2020-09-23').close.values[-1]
# print(bm_value)

# bm_value = ng.get_k_data(code='000300.SH', freq='d', start=t_date, end=t_date).close.values[-1]

# df_ = ng.get_k_data(code='000300.SH', freq='d', start='2019-09-23', end='2020-09-23')
# print(df_)

# history_data = df_.loc[df_["date"] <= '2020-04-20 00:00:00'][-30:].reset_index(drop=True)
# print(history_data)

# df_data = history_data.drop([0])
# print(df_data)

# df_data = history_data.iloc[:-1]
# print(df_data)



# df_data = history_data.drop([-1])
# print(df_data)
# body = {'table': 'C_EX_StockNetProfit',
#         'field_list': ['EndDate', 'StatisPeriod', 'StatisType', 'PNetProfitCount', 'PNetProfitAdd', 'PNetProfitReduce', 'ForecastYear'],
#         'alterField': 'EndDate',
#         'startDate': '2020-09-17',
#         'endDate': '2020-09-17',
#         'all_code': True}
#
# data = ng.get_fromCode(body)
# print(data)




# table = 'C_EX_DataStock'
# field_list = ["InnerCode","EndDate","StatisPeriod","ForecastYear","SecuCode","NetProfitAvg"]
#
# body = {
#     "table": table,
#     "field_list": field_list,
#     "alterField": "EndDate",
#     "startDate": "2020-07-05",
#     "endDate": "2020-07-07",
# }
# data = ng.get_fromDate(body=body)
# print(data)




# data = ng.get_ShareHolding(type='SZ', start='2021-04-07', end='2021-04-08')
# print(data)
# data = ng.get_ShareHolding(type='SH', start='2021-04-07', end='2021-04-08')
# print(data)
# data = ng.get_ShareHolding(type='HKSHSZ', start='2020-09-01', end='2020-09-28')
# print(data)





# data = ng.get_HKTradeCalendar(start='2020-09-01', end='2020-10-20')
# print(data)
#
# df_SZ = ng.get_ShareHolding(type='SZ', start='2020-10-09', end='2020-10-16')
# print(df_SZ)





# data = ng.get_stock_data(code='300940.SZ', freq='d',adj='qfq', end='2021-02-05',bars=2, innercode=249)
# print(data)



# data = ng.get_stock_data(code='000661.SH', freq='d',adj='qfq', end='2019-01-09',bars=2, innercode=249)
# print(data)


# data = ng.get_north_capital(start_date='2020-09-01', end_date='2020-09-01')
# print(data)


# data = ng.get_north_top10(start_date='2020-09-01', end_date='2020-09-01')
# print(data)


# stock_close_df = ng.get_stock_data(code='600175.SH', freq='d', adj='qfq', bars=1)
# print(stock_close_df)

# stock_close_df = ng.get_stock_data(code='600109.SH', freq='1m', adj='qfq', start='2019-10-09', end='2020-10-09')
# print(stock_close_df)

# stock_close_df = ng.get_stock_data(code='000661.SZ', freq='d', adj='qfq', end='2019-02-25', bars=1)
# print(stock_close_df)



# stock_close_df = ng.get_stock_data(code='000661.SZ', freq='d', adj='qfq', bars=1)
# print(stock_close_df)
#
# stock_close_df = ng.get_stock_data(code='000661.SZ', freq='d', adj='qfq', bars=1)['close'].tolist()[0]
# print(stock_close_df)
# print(type(stock_close_df))
# data = ng.get_stock_data(code='000661.SZ', freq='d', adj='qfq', bars=2)
# value = round(float(data.iloc[-1]['close']), 4)  # open_price
# print(value)



# print(stock_close_df['close'].tolist()[0])
# print(type(stock_close_df['close'].tolist()[0]))



# stock_close_df = ng.get_stock_data(code='000001.SZ', freq='d', adj='qfq', end='2020-10-25', bars=1)
# print(stock_close_df)



# stock_close_df = ng.get_stock_data(code='603058.SH', freq='d', adj='qfq', bars=1)
# print(stock_close_df)



# stock_close_df = ng.get_stock_data(code='603058.SH', freq='d', adj='qfq', start="2020-10-13",end="2020-10-13")
# print(stock_close_df)




# print(stock_close_df.shape)
# if stock_close_df.shape[0] > 0:  # 退市或停牌处理
#     print('asdas')



# data = ng.get_allPlate()
# print(data)
#
# d = h_raw = ng.get_plate_data_inner(code='880003', innercode=2000002, freq='d', adj='qfq', bars=300)
# print(d)



# data = ng.get_plate_data_inner(code=886219, innercode=2000500, freq='d', adj='qfq', bars=20)
# print(data)
#
# data = ng.get_plate_data_inner(code=886219, innercode=2000500, freq='d', adj='qfq', end='2020-09-01',bars=20)
# print(data)
#
# data = ng.get_plate_data_inner(code=886219, innercode=2000500, freq='d', adj='qfq', start='2020-08-05',end='2020-09-01')
# print(data)
#
# data = ng.get_plate_data_inner(code=886219, innercode=2000500, freq='d', adj='qfq', start='2020-09-01',end='2020-09-01')
# print(data)


# data = ng.get_allStock()
# print(data)
#
# # 获取A股所有股票代码+退市
# data = ng.get_allStockNew()
# print(data)



# data = ng.get_allStockData(adj='qfq',date='2020-10-23')
# print(data)



# ng.get_depth()


# a = ng.get_allStockData(adj='qfq',date='2012-02-22')
# print(a)


# a = ng.get_allStockData(adj='hfq',date='2020-10-30')
# print(a)
#
# a = ng.get_allStockData(date='2020-10-30')
# print(a)



# t11 = time.time()
# import ngwshare as ng

# # 获取全部基金
# a = ng.get_all_funds()
# print(a)
#
# a = ng.get_fund_data(code='510300.SH', innercode=5236, freq='d', adj='qfq', bars=20)
# print(a)
# # a = ng.get_fund_data(code='510300.SH', innercode=5236, freq='d', adj='qfq', end='2020-11-30', bars=20)
# # print(a)
# # a = ng.get_fund_data(code='510300.SH', innercode=5236, freq='d', adj='qfq', start='2020-11-02', end='2020-11-30')
# # print(a)
#
# # a = ng.get_fund_data(code='510300.SH', freq='d', adj='qfq', bars=20)
# # print(a)
# # a = ng.get_fund_data(code='510300.SH', freq='d', adj='qfq', end='2020-11-30', bars=20)
# # print(a)
# # a = ng.get_fund_data(code='510300.SH', freq='d', adj='qfq', start='2020-11-01', end='2020-11-30')
# # print(a)
#
# print(time.time()-t11)



t1 = time.time()

# a = ng.get_funds_depth(code='510300.SH')
# print(a)

# a = ng.get_funds_depth(code='510300.SH',innercode=5236)
# print(a)


# to_mail = 'wj296348304@163.com'
# mail_header = '【数据产品】【龙虎榜】'
# mail_content = '[信息]数据保存成功！！！'
# mail_flag = ng.send_mail(to_mail, mail_header, mail_content)
# print(mail_flag)

# h_last = ng.get_price(['000300.SH'])
# print(h_last)

# data = ng.get_stock_data(code='000001.SZ', freq='1m', adj='qfq', bars=3)
# print(data)
# data = ng.get_stock_data(code='000001.SH', freq='1m', adj='qfq', bars=3)
# print(data)




# # data = ng.get_allStock()
# # print(data)

# data = ng.get_all_funds()
# print(data)
# a = data.loc[data['TradingCode'] == '515050.SH']
# print(a)


# a = ng.get_allPlate()
# print(a)



# a = ng.get_funds_depth(code='150270.SZ',innercode=7548)
# print(a)
#
# a = data.loc[data['TradingCode'] == '150270.SZ']
# print(a)

#
# # code = '511880.SH'
# code = '510300.SH'
# a = data.loc[data['TradingCode'] == code]['InnerCode'].tolist()[0]
# print(a)
# print(type(a))



# a = data.loc[data['TradingCode'] == '150270.SZ']
# print(a)
#
# a = ng.get_fund_data(code='150270.SZ', innercode=5662, freq='d', adj='qfq', end='2020-11-30', bars=1)
# print(a)



# a = ng.get_fund_data(code='511880.SH', innercode=5662, freq='d', adj='qfq', end='2020-11-30', bars=1)
# print(a)


# a = ng.get_fund_data(code='511880.SH', innercode=5662, freq='d', adj='qfq', bars=1)
# print(a)

#
# bm_data = ng.get_fund_data(code='511880.SH', innercode=5662, freq='d', adj='qfq', bars=2)
# print(bm_data)
# bm_value = round(float(bm_data.iloc[-1]['close']), 4)
# print(bm_value)
#
# bm_data = ng.get_stock_data_inner(code='000300.SH', innercode=2131, freq='d', bars=2)
# print(bm_data)
# bm_value = round(float(bm_data.iloc[-1]['close']), 4)
# print(bm_value)


# data = ng.get_allStock()
# print(data)



# innercode = data.loc[data['code']=='000001.SH']['innercode'].tolist()[0]
# print(innercode)
# stock_close_df = ng.get_stock_data(code='000001.SH',innercode=innercode, freq='d', adj='qfq', bars=2)
# print(stock_close_df)
#
# value = round(float(stock_close_df.iloc[0]['close']), 4)
# print(value)
#
#
# open = stock_close_df['open'].tolist()[0]
# print(open)
# close = stock_close_df['close'].tolist()[0]
# print(close)


# bm_data = ng.get_stock_data_inner(code='000016.SH', innercode=2122, freq='d', bars=2)
# print(bm_data)
# bm_value = round(float(bm_data.iloc[-1]['close']), 4)
# print(bm_value)



# ng.get_plate_data_inner()
#
#
#
# bm_data = ng.get_stock_data(code='000016.SH', freq='d', adj='qfq', end='2020-10-23', bars=2)
# print(bm_data)
# print(bm_data['close'].tolist()[-1])
# bm_value = round(float(bm_data.iloc[-1]['close']), 4)
# print(bm_value)
#
# bm_value = ng.get_k_data(code='000016.SH', freq='d', start='2020-10-23', end='2020-10-23').close.values[-1]
# print(bm_value)



# a = ng.return_last_trading_day()
# print(a)

# data = ng.get_allStock()
# print(data)


a = ng.return_last_trading_day()
print(a)


# a = ng.get_allStockData(adj='qfq', date='2020-01-07')
# print(a)


# stock_close_df = ng.get_stock_data(code='600109.SH', freq='1m', adj='qfq', bars=200)
# print(stock_close_df)
# stock_close_df = ng.get_stock_data(code='600109.SH', freq='30m', adj='qfq', start='2015-12-07', end='2018-12-09')
# print(stock_close_df)
# stock_close_df = ng.get_stock_data(code='600109.SH', freq='1m', adj='qfq', start='2020-12-07 10:30:00', end='2020-12-09 14:30:00')
# print(stock_close_df)
# stock_close_df = ng.get_stock_data(code='600109.SH', freq='1m', adj='qfq', end='2020-12-09', bars=200)
# print(stock_close_df)
# stock_close_df = ng.get_stock_data(code='600109.SH', freq='1m', adj='qfq', end='2020-12-09 13:58:00', bars=200)
# print(stock_close_df)


# stock_close_df = ng.get_stock_data(code='600109.SH', freq='5m', adj='qfq', bars=200)
# print(stock_close_df)
# stock_close_df = ng.get_stock_data(code='600109.SH', freq='5m', adj='qfq', start='2020-11-09', end='2020-12-09')
# print(stock_close_df)
# stock_close_df = ng.get_stock_data(code='600109.SH', freq='5m', adj='qfq', start='2020-11-09 10:30:00',
#                                    end='2020-12-09 14:30:00')
# print(stock_close_df)
# stock_close_df = ng.get_stock_data(code='600109.SH', freq='5m', adj='qfq', end='2020-12-09', bars=200)
# print(stock_close_df)
# stock_close_df = ng.get_stock_data(code='600109.SH', freq='5m', adj='qfq', end='2020-12-09 14:00:00', bars=200)
# print(stock_close_df)


print(time.time()-t1)


# t_date = '2021-02-03'
# bm_value = ng.get_k_data(code='399006.SZ', freq='d', start=t_date, end=t_date).close.values[-1]
# print(bm_value)
#
# print(ng.get_k_data(code='399006.SZ', freq='d', start=t_date, end=t_date))
#
# bm_data = ng.get_stock_data_inner(code='399006.SZ', innercode=2121, freq='d', bars=2)
# print(bm_data)


# data = ng.get_stock_data_inner(code='000300.SH',innercode=2131, freq='d', bars=2)
# print(data)


# bm_value = ng.get_fund_data(code='511880.SH', innercode=5662, freq='d', adj='qfq', bars=2)
# print(bm_value)
#
# all_funds = ng.get_all_funds()
# print(all_funds)



# bm_value = round(float(bm_data.iloc[-1]['close']), 4)
# print(bm_value)


# a = ng.get_all_funds()
# print(a)
# b = a.loc[a.TradingCode=='515790.SH']
# print(b)
#
#
# c = ng.get_fund_data(innercode=95444,code='515790.SH',freq='d', adj='qfq',end='2021-02-03',bars=10)
# print(c)


# a = ng.sent_dingding2('asdasdasd',[13087005272],False)
# print(a)

# ng.sent_dingding2('【success】两融-综合数据！',[13087005272],False)
#
# ng.sent_dingding2('【success】两融-综合数据！',[13087005272],False)


# t_date = '2021-02-03'
#
# bm_value = ng.get_k_data(code='688004.SH', freq='d', start=t_date, end=t_date)
# print(bm_value)


# data = ng.get_hisTick(symbol='rb2103',exchange='SHFE',start='2021-02-01 13:30:00',end='2021-02-02 14:30:00')
# print(data)


