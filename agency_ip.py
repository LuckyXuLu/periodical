IPPOOL = []

import requests
import time
import threading
from requests.packages import urllib3


# 获取代理IP的线程类
class GetIpThread(threading.Thread):
    def __init__(self, apiUrl, fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond = fetchSecond
        self.apiUrl = apiUrl

    def run(self):
        while True:
            # 获取IP列表
            try:
                res = requests.get(self.apiUrl).content.decode()
                res = ' '.join(res.split())
                IPPOOL.append(res)
                # # 按照\n分割获取到的IP
                # IPPOOL = res.split('\n')

                if len(IPPOOL) >= 3:
                    print(IPPOOL)
                    IPPOOL_str = str(IPPOOL).replace("\'", "").replace("[", "").replace("]", "")
                    with open("ag_ip.txt", 'w') as f:
                        f.write(str(IPPOOL_str))
                    IPPOOL.pop(0)

                    # 休眠
                time.sleep(self.fetchSecond)

            except Exception as e:
                pass





if __name__ == '__main__':
    # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
    order = "****************"
    # 获取IP的API接口
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
    # 获取IP时间间隔，建议为5秒
    fetchSecond = 6
    # 开始自动获取IP
    GetIpThread(apiUrl, fetchSecond).start()
