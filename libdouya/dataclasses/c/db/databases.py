# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Dict,Any,List
from ....definations.cfg import DY_CONFIGURATION_KEY_DEF
from ...i.rdb import IDatabase

class Databases(object):
    def __init__(self, *databases:IDatabase):
        self.__database_info = { db.name : db for db in databases }

    def names(self) -> List[str]:
        return list(self.__database_info.keys())

    def db(self, name:str = None) -> IDatabase:
        if not name: name = DY_CONFIGURATION_KEY_DEF.PRIMARY_DATABASE[len(DY_CONFIGURATION_KEY_DEF.DATABASE)+1:]
        return self.__database_info.get(name)