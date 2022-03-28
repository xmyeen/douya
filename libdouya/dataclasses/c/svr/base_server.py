# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Dict,Any
from abc import ABCMeta, abstractclassmethod
from ..db import Databases

class BaseAsyncService(metaclass = ABCMeta):
    def __init__(self, name:str, dbs: Databases = None):
        self.__name = name
        self.__dbs = dbs
        self.__configuration = {}

    def __await__(self):
        yield from self.serve()

    @property
    def databases(self) -> Databases:
        return self.__dbs

    @property
    def configuration(self) -> Dict[str,Any]: 
        return self.__configuration

    @property
    def name(self) -> str:
        return self.__name

    @property
    def parallel_as(self) -> str:
        '''以什么方式进行并发，取值为范围mt/mp。
        '''
        return self.configuration.get('parallel_as')

    @property
    def worker_number(self) -> int:
        return int(self.configuration.get('worker_number', 1))

    @property
    def cron_text(self) -> str:
        return self.configuration.get('cron')

    @abstractclassmethod
    async def init(self): pass

    @abstractclassmethod
    async def serve(self): pass