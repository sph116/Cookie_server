# 超级鹰配置
CJY_USERNAME = ""
CJY_PASSWORD = ""


# redis相关设置
REDIS_HOST = "127.0.0.1"
REDIS_POET = 6379
REDIS_PSW = "123456"


# 各个网站的登录帐号信息
Accounts = {
    "zhihu": {
        "username": "",     # 知乎登录账号
        "password": "",     # 知乎登录尼玛
        "cookie_key": "",   # redis 存储cookie key值
        "max_cookie_nums": 0,   # 最大cookie数量
        "chect_interval": 0   # 检测周期/秒
    },

}
