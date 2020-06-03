#1. cookie保存在redis中使用什么数据结构
#2. 数据结构应该满足: 1. 可以随机获取  2. 可以防止重复  -set


#1. 如何确保每一个网站的都会被单独运行

import redis
import settings
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed   # 线程池模块
from functools import partial


class CookieServer():
    def __init__(self, settings):

        self.redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_POET, password=settings.REDIS_PSW)
        self.service_list = []
        self.settings = settings

    def register(self, cls):
        self.service_list.append(cls)

    def login_service(self, srv):
        """
        用于登录网站 获取cookie 入库
        :param srv:
        :return:
        """
        while 1:
            srv_cli = srv(settings)
            srv_name = srv_cli.name
            cookie_dict = srv_cli.login()
            cookie_nums = self.redis_cli.scard(self.settings.Accounts[srv_name]["cookie_key"])    # 查询当前账户的cookie数量
            if cookie_nums < self.settings.Accounts[srv_name]["max_cookie_nums"]:  # 若小于定义的cookie数量
                cookie_dict = srv_cli.login()   # 登录获取cookie_dict
                self.redis_cli.sadd(self.settings.Accounts[srv_name]["cookie_key"], json.dumps(cookie_dict))
            else:
                print(f"{srv_name} 的cookie池已满, 等待十秒")
                time.sleep(10)


    def check_cookie_service(self, srv):
        """
        检测cookie池中的cookie
        :param srv:
        :return:
        """
        while 1:
            print("开始检测cookie是否可用")
            srv_cli = srv(settings)
            srv_name = srv_cli.name
            all_cookies = self.redis_cli.smembers(self.settings.Accounts[srv_name]["cookie_key"])  # 提取所有的cookie
            print("目前可用cookie数量:{}".format(len(all_cookies)))
            for cookie_str in all_cookies:
                print("获取到cookie:{}".format(cookie_str))
                cookie_dict = json.loads(cookie_str)
                valid = srv_cli.check_cookie(cookie_dict)  # 对当前的cookie进行检测
                if valid:
                    print("cookie 有效")
                else:
                    print("cookie已经失效. 删除cookie")
                    self.redis_cli.srem(self.settings.Accounts[srv_name]["cookie_key"], cookie_str)    # 若cookie失效 则删除此cookie

            interval = self.settings.Accounts[srv_name]["chect_interval"]
            print(f"{interval}s 后重新检测cookie")
            time.sleep(interval)   # 休眠


    def start(self):
        task_list = []
        print("启动登录服务")
        login_executor = ThreadPoolExecutor(max_workers=5)   # 定义登录线程池
        for srv in self.service_list:
            task = login_executor.submit(partial(self.login_service, srv))   # 启动线程 使用partial将函数与参数封装为函数名字
            task_list.append(task)  # 加入线程池

        check_executor = ThreadPoolExecutor(max_workers=5)  # 定义cookie检测线程池
        for srv in self.service_list:
            task = check_executor.submit(partial(self.check_cookie_service, srv))
            task_list.append(task)

        for future in as_completed(task_list):
            data = future.result()
            print(data)








