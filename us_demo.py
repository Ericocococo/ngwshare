__author__ = 'wangjian'

import ngwshare as ng

data = ng.get_USKline(symbol='dia',klineType='day',count=20)
print(data)

data = ng.get_USKline(symbol='dia',klineType='day',end='2021-02-01',count=20)
print(data)



# a = ng.get_USKline(symbol='dia',klineType='Week',count=20)
# print(a)
#
# a = ng.get_USKline(symbol='dia',klineType='Week',end='2021-02-03',count=20)
# print(a)







