# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import ABCMeta, abstractclassmethod
from ..rdb import IDatabase

class IDatabaseConfiger(metaclass = ABCMeta):
    def __init__(self):
        pass

    @abstractclassmethod
    def init_db(db:IDatabase,  name:str = None):
        pass