__author__ = 'wangjian'

from pymongo import MongoClient

def conn_mongo(sql_info=None):
    host = sql_info.get('host')
    port = sql_info.get('port')
    DB_CONN = MongoClient('mongodb://{}:{}'.format(host,port))
    return DB_CONN


if __name__ == '__main__':
    import pandas as pd

    # 测试
    sql_info = {
        'host': '192.168.3.160',
        'port': '27017'
    }
    DB_CONN = conn_mongo(sql_info)
    collection = DB_CONN['Strategy']['DK_Minute_TimeIntervalN_1']
    data_raw = collection.find(
        {'InnerCode': 7,
         'TimeStr': {'$max': 1}})
    df_data = pd.DataFrame(list(data_raw))
    print(df_data)