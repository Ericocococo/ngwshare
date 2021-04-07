__author__ = 'wangjian'
from ngwshare.utils.http_util import get_ua
import requests
import traceback
import json
import pandas as pd


def get_GuBaTieZiList(varietyId=None,startTime=None,endTime=None):
    try:
        url = "https://dev-taojinuser.inquant.cn/analystsstgy/guba/GetPostList?varietyId={}&starttime={}&endtime={}"\
            .format(varietyId,startTime,endTime)
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('error_no') == 0:
                return pd.DataFrame(response_json.get('data'))
            else:
                return None
        except:
            return None


def get_GuBaTieZiDetail(postId=None):
    try:
        url = "https://dev-taojinuser.inquant.cn/analystsstgy/guba/GetPostDetail?postId={}".format(postId)
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('error_no') == 0:
                return response_json.get('data')
            else:
                return None
        except:
            return None


def get_GuBaReplyList(varietyId=None,startTime=None,endTime=None):
    try:
        url = "https://dev-taojinuser.inquant.cn/analystsstgy/guba/GetReplyList?varietyId={}&starttime={}&endtime={}"\
            .format(varietyId,startTime,endTime)
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('error_no') == 0:
                return pd.DataFrame(response_json.get('data'))
            else:
                return None
        except:
            return None


def get_GuBaReplyDetail(postId=None):
    try:
        url = "https://dev-taojinuser.inquant.cn/analystsstgy/guba/GetReplyByPostId?postId={}".format(postId)
        headers = {'User-Agent': get_ua()}
        response = requests.get(url, headers=headers)
        response.close()
    except Exception:
        print(traceback.format_exc())
    else:
        try:
            response_json = json.loads(response.content.decode())
            # print(response_json)
            if response_json.get('error_no') == 0:
                return response_json.get('data')
            else:
                return None
        except:
            return None



if __name__ == '__main__':
    import ngshare as ng

    # 获取帖子列表
    data = ng.get_GuBaTieZiList(varietyId=10, startTime='2021-03-01', endTime='2021-03-10')
    print(data)
    # 根据帖子id获取帖子详情
    data = ng.get_GuBaTieZiDetail(postId=1008152146)
    print(data)

    # 获取回复列表
    data = ng.get_GuBaReplyList(varietyId=10, startTime='2021-03-01', endTime='2021-03-10')
    print(data)
    # 根据帖子id获取回复详情
    data = ng.get_GuBaReplyDetail(postId=1008152146)
    print(data)

















