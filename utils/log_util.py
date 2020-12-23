# # 日志输出到文件
# import logging
# import datetime
#
# logger = logging.getLogger()
#
# # a 追加   w 覆盖
# logging.basicConfig(
#     level=logging.INFO,
#     # filename='/home/wj/Desktop/STQDataApi/web/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='./log/{}.txt'.format(str(datetime.datetime.now().date())),
#
#     # filename='/home/wangjian/software/python3.7/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     filename='/home/wangjian/.local/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#
#     # filename='/usr/local/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='C:\\Program Files\\python\\python37\Lib\\site-packages\\ngshare\\log\\{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='D:\\anaconda\Lib\\site-packages\\ngshare\\log\\{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='D:\\Anaconda3\\Lib\\site-packages\\ngshare\\log\\{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='D:\\anaconda3.8\\Lib\\site-packages\\ngshare\\log\\{}.txt'.format(str(datetime.datetime.now().date())),
#
#     # 券商
#     # filename='/home/admin/codes/software/python3.7/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#
#
#     # filename='/home/wangjian/.virtualenvs/strategy1/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='/home/wangjian/.virtualenvs/strategy2/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='/home/wangjian/.virtualenvs/strategy3/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='/home/wangjian/.virtualenvs/strategy4/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='/home/wangjian/.virtualenvs/strategy5/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='/home/wangjian/.virtualenvs/strategy6/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     # filename='/home/wangjian/.virtualenvs/strategy7/lib/python3.7/site-packages/ngshare/log/{}.txt'.format(str(datetime.datetime.now().date())),
#     filemode='a+',
#     format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:%(message)s")
#
# if __name__ == '__main__':
#     def print(message1=None,message2=None,message3=None,message4=None):
#         str1 = ''
#         if message1:
#             str1 = str(message1)
#         if message2:
#             str1 = str(message1)+str(message2)
#         if message3:
#             str1 = str(message1)+str(message2)+str(message3)
#         if message4:
#             str1 = str(message1)+str(message2)+str(message3)+str(message4)
#         logger.info(str1)
#
#
#     # logger.debug('11111111111..........')
#     # logger.info('222222222.............')
#     # logger.warning('333333333...........')
#     # logger.error('44444444444..............')
#     # logger.critical('55555555555............')
#
#     print([1,32,1], "%s只股票没检索到行业名称" % len([0,21,123]))
#     print('asdasd')
