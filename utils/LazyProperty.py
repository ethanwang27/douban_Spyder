# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/15 11:22
@File: LazyProperty.py
@Project: Proxy-Pool
@Description: None
"""


class LazyProperty(object):
    """
    延迟初始化
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        value = self.func(instance)
        setattr(instance, self.func.__name__, value)
        return value

