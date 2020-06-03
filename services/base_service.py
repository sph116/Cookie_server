# class BaseService():
#     pass
#     # 方法1. 为了让子类强制写login 在父类方法中抛出异常
#     def login(self):
#         raise NotImplemented
import abc

class BaseService(metaclass=abc.ABCMeta):
    pass
    # 方法2. 使用抽象基类
    @abc.abstractmethod
    def login(self):
        pass

    @abc.abstractmethod
    def check_cookie(self, cookie_dict):
        pass


class Lagou(BaseService):
    name = "lagou"
    # 强制性的效果
    # def login(self):
    #     print("login in {}".format(self.name))

if __name__ == "__main__":
    l = Lagou()
    l.login()

