import ngwshare as ng
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows',5000)
pd.set_option('display.max_columns',5000)
pd.set_option('display.width',10000)


# # 获取所有场外基金代码
# data = ng.get_AllOTCFundsInfo()
# print(data.loc[:300])
# df = data

# a = df[df['FundCode'] == '000879']['FundName'].tolist()[0]
# print(a)

# a = ng.get_k_data(code='000300.SH', freq='d', start='2021-01-28', end='2021-01-28').close.values[0]
# print(a)

# # 净值
# data = ng.get_OTCFundsValues(code='000003',start='2020-10-13',end='2021-01-18')
# print(data)



code = '000879'


# # 简要信息
# data = ng.get_OTCFundsInfo(innercode=22035)
# print(data)

# OTC_DATA_i = ng.get_OTCFundsValues(code="000003", start="2013-10-13", end="2021-01-22")
# print(OTC_DATA_i)

# inn = 95061
# # 净值
# data = ng.get_OTCFundsValues(innercode=inn)
# print(data)
# # 简要信息
# data = ng.get_OTCFundsInfo(innercode=inn)
# print(data)



# data = ng.get_OPF_Bouns(code=code)
# print(data)










def deal_adjprice(etfcode,startday,endday):
    OTC_DATA_i = ng.get_OTCFundsValues(code=etfcode, start=startday, end=endday)
    # print(OTC_DATA_i)
    OTC_DATA_i["Date"] = pd.to_datetime(OTC_DATA_i["Date"])
    OTC_DATA_i.sort_values(by="Date", ascending=True, inplace=True)
    print(OTC_DATA_i)

    Bouns_i = ng.get_OPF_Bouns(code=etfcode)
    Bouns_i["ChuXiDate"] = pd.to_datetime(Bouns_i["ChuXiDate"])
    # Bouns_i["Date"] = [last_trading_day(date, tradingdays) for date in Bouns_i["ChuXiDate"]]
    Bouns_i["Date"] = Bouns_i["ChuXiDate"]
    # print(Bouns_i)

    flag = (Bouns_i["Date"]>=pd.to_datetime(startday))&(Bouns_i["Date"]<=pd.to_datetime(endday))
    # print(flag)
    # print(type(flag))

    Bouns_i = Bouns_i[flag]
    print(Bouns_i)

    OTC_DATA_i = pd.merge(OTC_DATA_i,Bouns_i.loc[:,["Date","Bonus"]],how="outer")
    print(OTC_DATA_i)

    OTC_DATA_i["Bonus"].fillna(0,inplace=True)
    print(OTC_DATA_i)

    # OTC_DATA_i["PerNetValue_1"] = OTC_DATA_i["PerNetValue"] - OTC_DATA_i["Bonus"]
    # OTC_DATA_i["PerNetValue_1"] = OTC_DATA_i["PerNetValue_1"].shift(1)
    # OTC_DATA_i["rets"] = OTC_DATA_i["PerNetValue"]*1.0/OTC_DATA_i["PerNetValue_1"] - 1
    OTC_DATA_i["rets"] = (OTC_DATA_i["PerNetValue"] + OTC_DATA_i["Bonus"])/OTC_DATA_i["PerNetValue"].shift(1) - 1
    print(OTC_DATA_i)

    OTC_DATA_i["rets"][0] = 0
    print(OTC_DATA_i)

    OTC_DATA_i["hfq_price"] = OTC_DATA_i["rets"] + 1
    print(OTC_DATA_i)

    PerNetValue0 = OTC_DATA_i["PerNetValue"][0]
    print(PerNetValue0)

    print(OTC_DATA_i["hfq_price"])
    print(OTC_DATA_i["hfq_price"].cumprod())

    OTC_DATA_i["hfq_price"] = OTC_DATA_i["hfq_price"].cumprod() * PerNetValue0
    print(OTC_DATA_i)

    PerNetValue_1 = list(OTC_DATA_i["PerNetValue"])[-1]
    print(PerNetValue_1)
    hfqprice_1 = list(OTC_DATA_i["hfq_price"])[-1]
    OTC_DATA_i["qfq_price"] = OTC_DATA_i["hfq_price"]/hfqprice_1*PerNetValue_1

    return OTC_DATA_i




adjprice = deal_adjprice(code,'2020-05-01','2020-12-30')
print(adjprice)










