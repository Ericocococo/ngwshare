
__author__ = 'wangjian'
import pyodbc

from ngshare.constants import ODBC_D

class ODBC:
    def __init__(self,server,uid,pwd,db,DRIVER='{SQL Server}'):
        self.server = server
        self.uid = uid
        self.pwd = pwd
        self.db = db
        # self.DRIVER = '/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.1.so.9.2'
        # self.DRIVER = '/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1'  # ubuntu
        self.DRIVER = ODBC_D

    def GetConnect(self):
        if not self.db:
            raise(NameError,'没有设置数据库信息')
        self.conn = pyodbc.connect(SERVER=self.server,UID=self.uid,PWD=self.pwd,DATABASE=self.db,DRIVER=self.DRIVER)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,'连接数据库失败')
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


def conn_sqlserver_select(sql=None,sql_info=None):
    host = sql_info.get('host')
    database = sql_info.get('database')
    user = sql_info.get('user')
    password = sql_info.get('password')

    ms = ODBC(server=host, uid=user, pwd=password, db=database)
    # ms = ODBC(server=SQL_SERVER_DOMAIN, uid=SQL_SERVER_ACCOUNT, pwd=SQL_SERVER_PASSWORD, db=SQL_SERVER_DATABASE_NAME)
    row = ms.ExecQuery(sql)
    # print(row)
    return row


def conn_sqlserver_insert(sql=None,sql_info=None):
    host = sql_info.get('host')
    database = sql_info.get('database')
    user = sql_info.get('user')
    password = sql_info.get('password')

    ms = ODBC(server=host, uid=user, pwd=password, db=database)
    # ms = ODBC(server=SQL_SERVER_DOMAIN, uid=SQL_SERVER_ACCOUNT, pwd=SQL_SERVER_PASSWORD, db=SQL_SERVER_DATABASE_NAME)
    ms.ExecNonQuery(sql)
    # print('插入成功.')



if __name__ == '__main__':
    import datetime
    import ngshare as ng
    import time
    import pandas as pd

    # # 测试
    # sql_info = {
    #     'host': '192.168.3.112',
    #     'database': 'DB_IQNgwStrategy',
    #     'user': 'sa',
    #     'password': 'taotao778899!',
    # }
    # # # 生产
    # # sql_info = {
    # #     'host': 'ngwstrategy.mssql.niuguwang',
    # #     'database': 'DB_IQNgwStrategy',
    # #     'user': 'sa',
    # #     'password': 'taotao778899!',
    # # }


    # # 测试
    # sql_info = {
    #     'host': '192.168.3.112',
    #     'database': 'DB_IndependentAccount',
    #     'user': 'sa',
    #     'password': 'taotao778899!',
    # }
    # # # 生产
    # # sql_info = {
    # #     'host': 'ngwstrategy.mssql.niuguwang',
    # #     'database': 'DB_IndependentAccount',
    # #     'user': 'sa',
    # #     'password': 'taotao778899!',
    # # }



    # 测试
    sql_info = {
        'host': '192.168.3.112',
        'database': 'DB_INFORMATION',
        'user': 'sa',
        'password': 'taotao778899!',
    }
    # # 生产
    # sql_info = {
    #     'host': '192.168.2.55',
    #     'database': 'DB_INFORMATION',
    #     'user': 'sa',
    #     'password': 'taotao778899!',
    # }

    t1 = time.time()


    sql = """select InnerCode,FundCode,FundName,RegisterDate,Bonus from FundBonus;"""
    # sql = """select InnerCode,FundCode,FundName,SplitDate,SplitRate from FundSplit;"""
    data = conn_sqlserver_select(sql=sql,sql_info=sql_info)
    data_list = []
    for i in data:
        doc = {
            'innercode':int(i[0]),
            'code': str(i[1]),
            'name': str(i[2]),
            'date': str(i[3])[:10],
            'num': round(float(i[4]),4),
        }
        data_list.append(doc)
    df_data = pd.DataFrame(data_list)
    print(df_data)

    symbol = '511880.SH'
    print(symbol[:6])
    # df_data_code = df_data.loc[df_data['code'] == symbol[:6]].sort_values(["date"], ascending=False)
    df_data_code = df_data.loc[df_data['code'] == symbol[:6]].sort_values(["date"], ascending=False).head(1)
    print(df_data_code)


    print(time.time()-t1)





























