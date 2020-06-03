# Cookie_server
知乎模拟登录 cookie池


启动:
因知乎会检测selenium特征值 使用手动方式启动chrome 并关联 selenium

cd进入chrome.exe路径 
chrome.exe --remote-debugging-port=9222

因知乎 登录 随机出现倒立文字验证码/普通文字验证码
1.倒立文字识别使用 zhiye库
2.文字验证码 调用超级🦅付费接口

需配置:
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
        "max_cookie_nums": 0,   # cookie池数量
        "chect_interval": 0   # 检测周期/秒
    },

}
