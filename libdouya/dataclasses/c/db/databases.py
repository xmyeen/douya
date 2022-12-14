# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import List
from ....definations.cfg import DY_CONFIGURATION_KEY_DEF
from ...i.rdb import IDatabaseProxy, IDatabases

class Databases(IDatabases):
    def __init__(self, *databases:IDatabaseProxy):
        IDatabases.__init__(self)
        self.__database_info = { db.code_name : db for db in databases }

    @property
    def code_names(self) -> list[str]:
        return list(self.__database_info.keys())

    def db(self, code_name:str|None = None) -> IDatabaseProxy|None:
        return self.__database_info.get(code_name or DY_CONFIGURATION_KEY_DEF.PRIMARY_DATABASE[len(DY_CONFIGURATION_KEY_DEF.DATABASE)+1:])