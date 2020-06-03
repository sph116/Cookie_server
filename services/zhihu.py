# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from mouse import move, click
from selenium.webdriver.common.keys import Keys
import base64
from services.common import chaojiying
from zheye import zheye
from services.base_service import BaseService
import settings
import requests

class ZhihuLoginService(BaseService):
    name = "zhihu"

    def __init__(self, settings):
        self.user_name = settings.Accounts[self.name]["username"]
        self.password = settings.Accounts[self.name]["password"]
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.browser = webdriver.Chrome('C:/Users/孙佩豪/AppData/Local/Google/Chrome/Application/chromedriver.exe',
                                   options=chrome_options)

    def cheeck_login(self):
        try:
            # self.browser.get('https://www.zhihu.com')  # 打开知乎登录页面
            time.sleep(5)
            self.browser.find_element_by_xpath(
                '//div[@class="Popover PushNotifications AppHeader-notifications"]')  # 是否登录成功
            return True
        except Exception as e:
            return False

    def check_cookie(self, cookie_dict):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        }

        res = requests.get('https://www.zhihu.com/', headers=headers, cookies=cookie_dict, allow_redirects=False)
        if res.status_code != 200:
            return False
        else:
            return True



    def login(self):
        try:
            self.browser.maximize_window()  # 最大化窗口
        except:  # 已最大化的情况 代码会出错 捕获错误
            pass

        while not self.cheeck_login():

            self.browser.get('https://www.zhihu.com/signin')  # 打开知乎登录页面
            time.sleep(5)
            move(914, 329)  # 点击 帐号密码登录
            click()
            time.sleep(2)
            self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                Keys.CONTROL + "a")                              # 全选 然后输入账户密码
            self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(self.user_name)
            self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
            self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(self.password)
            move(955, 566)
            click()

            if self.cheeck_login():
                Cookies = self.browser.get_cookies()  # 获取登录成功的cookie
                print(Cookies)
                cookie_dict = {}
                import pickle
                for cookie in Cookies:
                    cookie_dict[cookie['name']] = cookie['value']
                # self.browser.close()  # 暂时不关闭
                return cookie_dict

            else:


                try:
                    english_captcha_element = self.browser.find_element_by_class_name("Captcha-englishImg")  # 是否出现英文验证码
                except:
                    english_captcha_element = None

                try:
                    chinese_captcha_element = self.browser.find_element_by_class_name("Captcha-chineseImg")  # 是否出现中文验证码
                except:
                    chinese_captcha_element = None

                if chinese_captcha_element:  # 如果产生中文验证码
                    time.sleep(1)
                    ele_position = chinese_captcha_element.location  # 获取节点坐标
                    x_relative = ele_position["x"]  # x坐标
                    y_relative = ele_position["y"]  # y坐标

                    browser_navigation_panel_height = self.browser.execute_script(
                        'return window.outerHeight - window.innerHeight;')  # 浏览器上栏高度
                    browser_navigation_panel_height = 70

                    time.sleep(3)
                    base64_text = chinese_captcha_element.get_attribute("src")  # 提取中文验证码节点的arc属性
                    code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")  # 消除图片bs64编码中的无用符号
                    fh = open("yzm_cn.jpeg", "wb")  # 保存文件
                    fh.write(base64.b64decode(code))
                    fh.close()

                    z = zheye()
                    positions = z.Recognize('yzm_cn.jpeg')  # 使用者也 提取倒立文字坐标

                    last_position = []
                    if len(positions) == 2:
                        if positions[0][0] > positions[1][0]:  # 按照顺序排列倒立文字坐标
                            last_position.append([positions[1][0], positions[1][1]])
                            last_position.append([positions[0][0], positions[0][1]])
                        else:
                            last_position.append([positions[0][0], positions[0][1]])
                            last_position.append([positions[1][0], positions[1][0]])

                    if len(positions) == 2:
                        first_position = [int(last_position[0][1] / 2) + x_relative, int(last_position[0][
                                                                                             0] / 2) + y_relative + browser_navigation_panel_height]  # 实际页面中 倒立文字图片为正常图片缩放的一倍 所有坐标需要除2取整 来获得可以在页面中使用的坐标
                        second_position = [int(last_position[1][1] / 2) + x_relative,
                                           int(last_position[1][0] / 2) + y_relative + browser_navigation_panel_height]

                        move(first_position[0], first_position[1])  # 坐标 起始点x坐标+倒立文字x坐标   起始点y坐标+浏览器地址栏高度+倒立文字y坐标
                        click()

                        move(second_position[0], second_position[1])
                        click()

                    else:  # 如果只有一个倒立文字
                        last_position.append([positions[0][1], positions[0][1]])
                        first_position = [int(last_position[0][1] / 2) + x_relative,
                                          int(last_position[0][0] / 2) + browser_navigation_panel_height + y_relative]
                        time.sleep(5)
                        move(first_position[0], first_position[1])
                        time.sleep(5)
                        click()

                    self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                        Keys.CONTROL + "a")  # 全选 然后输入账户密码
                    self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(self.user_name)
                    self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                    self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(self.password)
                    move(954, 619)
                    click()

                if english_captcha_element:  # 如果产生英文验证码
                    time.sleep(1)
                    base64_text = english_captcha_element.get_attribute("src")
                    code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")  # 消除图片bs64编码中的无用符号
                    fh = open("yzm_en.jpeg", "wb")    # 保存文件
                    fh.write(base64.b64decode(code))
                    fh.close()

                    cjy_cli = chaojiying.Chaojiying_Client(settings.CJY_USERNAME, settings.CJY_PASSWORD, '96001')
                    im = open('yzm_en.jpeg', "rb").read()
                    json_data = cjy_cli.PostPic(im, 1902)
                    if json_data["err_no"] == 0:
                        print("识别成功！")
                        code = json_data["pic_str"]
                        print(json_data["pic_str"])

                    else:
                        print("识别失败，继续尝试！")
                        return

                    # while True:  # 若识别失败 不停识别 直至成功
                    #     if code == "":  #
                    #         code = Yundama.decode("yzm_en.jpeg", 5000, 60)
                    #         time.sleep(0.5)
                    #     else:
                    #         break

                    self.browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div/label/input').send_keys(Keys.CONTROL + "a")  # 找到英文验证码位置
                    self.browser.find_element_by_xpath(
                        '//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div/label/input').send_keys(code)
                    move(956, 600)
                    click()

                time.sleep(5)


        Cookies = self.browser.get_cookies()  # 获取登录成功的cookie
        cookie_dict = {}
        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
        # self.browser.close()   # 暂时不关闭
        return cookie_dict



if __name__ == "__main__":
    import settings
    zhigu = zhihu = ZhihuLoginService(settings)
    cookie_dict = zhihu.login()
    print(cookie_dict)


    import requests

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }

    res = requests.get('https://www.zhihu.com/', headers=headers, cookies=cookie_dict, allow_redirects=False)
    print(res.text)

