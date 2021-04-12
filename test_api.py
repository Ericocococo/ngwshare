__author__ = 'wangjian'

import requests
import json
import traceback
import random
import pandas as pd


def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        "(Windows NT 6.1; WOW64)", "(Windows NT 10.0; WOW64)", "(X11; Linux x86_64)",
        "(Macintosh; Intel Mac OS X 10_12_6)"
    ]
    chrome_version = "Chrome/{}.0.{}.{}".format(first_num, third_num, fourth_num)
    ua = " ".join(["Mozilla/5.0", random.choice(os_type), "AppleWebKit/537.36",
                   "(KHTML, like Gecko)", chrome_version, "Safari/537.36"])
    return ua



def get_OPF_Bouns(code=None):
    url = 'https://stq.niuguwang.com/funds/Bonus?code={}'.format(code)
    # print(url)
    try:
        headers = {"Content-Type": "application/json",
                   'User-Agent':get_ua()}
        response = requests.get(url, headers=headers).content.decode()
        response_json = json.loads(response)
        df_data = pd.DataFrame(response_json['data'])
        return df_data[['FundCode','DengJiDate','ChuXiDate','FaFangDate','Bonus','Bonus','AddTime']]\
            .sort_values(by=["ChuXiDate"],ascending=[False])
    except Exception:
        print(traceback.format_exc())



if __name__ == '__main__':
    import ngwshare as ng
    import datetime

    code = '000001'
    data = ng.get_OPF_Bouns(code=code)
    print(data)


