__author__ = 'wangjian'
import ngwshare as ng


# 获取所有 机器人id
data = ng.get_all_robots_info()
print(data)


# # # 停止某个机器人
# data = ng.stop_robot(robotId=101)
# print(data)


# # 获取机器人的持仓
# data = ng.get_robot_position(stgyAccount=34,symbol_exchange='cu2101.SHFE',posSide=2)
# print(data)
# # {'data': {'stgyPosId': 22, 'stgyAccount': 1, 'symbol': 'rb2101', 'exchange': 4, 'quantity': 1, 'forzen': 0, 'todayPositon': 0, 'todayForzen': 0, 'posSide': 1, 'margin': 5292.3, 'costPx': 3928.0, 'openCostPx': 3930.0, 'profit': 0.0, 'updateTime': '2020-11-30 10:32:16'}, 'error_no': 0, 'error_info': ''}
# data = ng.get_robot_position(stgyAccount=1,symbol_exchange='ag2101.SHFE',posSide=1)
# print(data)
# # {'data': None, 'error_no': 0, 'error_info': ''}


# # 获取机器人的上一日的equity
# data = ng.get_RobotLastEquity(robotId=40)
# print(data)




# # 机器人 下单
# data = ng.OmsContract_CreateOrder(stgyAccountId=34,stgySignalId=33,symbol_exchange='cu2101.SHFE',side='close_short',quantity=1,is_today=True)
# print(data)
# # {'data': 118, 'error_no': 0, 'error_info': ''}
# # {'data': 0, 'error_no': 1, 'error_info': '机器人已停止'}


# # # 机器人 查询订单状态
# data = ng.OmsContract_GetOrderStatus(stgyOrderId=299)
# print(data)
# # {'data': {'stgyOrderId': 118, 'stgyAccount': 1, 'stgySignalId': 12, 'orderId': '298054-SHFE_1000110_060031', 'symbol': 'ag2101', 'exchange': 4, 'orderSide': 66, 'offset': 1, 'quantity': 4, 'price': 1.0, 'filled': 4, 'orderTime': '2020-11-30 11:11:19', 'orderType': 1, 'tradeDate': '2020-11-30 00:00:00', 'updateTime': '2020-11-30 11:11:21', 'status': 5, 'note': '完全成交'}, 'error_no': 0, 'error_info': ''}


# # 机器人 撤单
# data = ng.OmsContract_CancelOrder(stgyAccountId=1, stgyOrderId=123)
# print(data)

# # {'error_no': 0, 'error_info': 'OK'}
# # {'error_no': 1, 'error_info': '无效的策略单id'}








