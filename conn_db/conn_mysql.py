__author__ = 'wangjian'

from pymysql import connect


def conn_mysql_select(sql=None,sql_info=None):
    host = sql_info.get('host')
    port = sql_info.get('port')
    database = sql_info.get('database')
    user = sql_info.get('user')
    password = sql_info.get('password')

    conn = connect(host=host, port=port, database=database, user=user, password=password, charset='utf8')


    cs1 = conn.cursor()
    cs1.execute(sql)

    data = cs1.fetchall()

    cs1.close()
    conn.close()
    return data


def conn_mysql_insert(sql=None,sql_info=None):
    host = sql_info.get('host')
    port = sql_info.get('port')
    database = sql_info.get('database')
    user = sql_info.get('user')
    password = sql_info.get('password')

    conn = connect(host=host, port=port, database=database, user=user, password=password, charset='utf8')

    # conn = connect(host='localhost', port=3306, database='ngw_strategy', user='root', password='mysql', charset='utf8')
    # conn = connect(host='192.168.3.215',port=3306,database='ngw_strategy',user='tjlh',password='L*P30wk|dvhdR',charset='utf8')
    # conn = connect(host='stq.mysql.ngw.zw.in', port=3306, database='ngw_strategy', user='tjlh',password='tjXx^Egw3NdnLK', charset='utf8')
    cs1 = conn.cursor()

    cs1.execute(sql)
    conn.commit()
    # logger.info('插入成功.')
    print('插入成功.')
    cs1.close()
    conn.close()



