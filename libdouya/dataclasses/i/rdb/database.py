# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Any, List, Dict
from contextlib import contextmanager

#*data_records:Any

# class IDatabaseSession(object, metaclass = ABCMeta):
#     def __init__(self): pass

#     def map(self, Callable[]) -> "IDatabaseSession": pass

#     def filter(self) -> "IDatabaseSession": pass

#     def for_each(self) -> "IDatabaseSession": pass

#     def or_else(self, default_value:Any) -> Any: pass

#     def or_else_get(self) -> Any: pass

# def make_table_declarative_entity(id:str, ctx:Any) -> Any:
#     pass

class IDatabaseProxy(metaclass = ABCMeta):
    def __init__(self): pass

    @property
    @abstractmethod
    def code_name(self) -> str:
        '''数据库代号'''

    @property
    @abstractmethod
    def configuration(self) -> dict[str,Any]:
        '''配置'''
    # @configuration.setter
    # @abstractmethod
    # def configuration(self, val: dict[str,Any]):
    #     pass

    @property
    @abstractmethod
    def connection_url(self) -> str:
        '''连接信息'''

    @property
    @abstractmethod
    def connection_options(self) -> list[str]:
        '''连接选项'''

    @property
    @abstractmethod
    def is_debugging(self) -> bool: 
        '''是否调试模式'''

    @property
    @abstractmethod
    def internal_implementation(self) -> Any: 
        '''内部实现'''

    @property
    @abstractmethod
    def declarative(self) -> 'IDatabaseDeclarative': 
        '''数据库代号'''

    @abstractmethod
    def connect(self, enable_scheme_rebuiding:bool):
        '''连接数据库
        '''

    @abstractmethod
    def establish_connection(self):
        '''连接数据库
        '''

    @abstractmethod
    def initialize(self):
        '''初始化
        '''

    @contextmanager
    @abstractmethod
    def on_session(self) -> Any:
        pass

    @contextmanager
    @abstractmethod
    def on_transactional_session(self) -> Any:
        pass

class IDatabaseDeclarative(metaclass = ABCMeta):
    def __init__(self): pass

    @property
    @abstractmethod
    def code_name(self) -> str: 
        '''数据库代号'''

    @property
    @abstractmethod
    def table(self) -> Any: 
        '''表的描述'''

    @property
    @abstractmethod
    def internal_implementation(self) -> Any: 
        '''内部实现'''

    @abstractmethod
    def make_proxy(self, **configuration:Any) -> IDatabaseProxy: pass

class IDatabases(object):
    def __init__(self): pass

    @property
    @abstractmethod
    def code_names(self) -> list[str]:
        '''代号列表'''

    @abstractmethod
    def db(self, code_name:str|None = None) -> IDatabaseProxy: pass
