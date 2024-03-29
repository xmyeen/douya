# -*- coding:utf-8 -*-
#!/usr/bin/env python

from ....dataclasses.i.rdb import IDatabaseDeclarative, IDatabaseTable
from ....definations.cfg import DY_CONFIGURATION_KEY_DEF
from ...mgr import NamingMgr

def make_db_declarative(orm_name:str, id: str|None = None, base_class: type[IDatabaseTable]|None = None) -> IDatabaseDeclarative:
    if not id: id = DY_CONFIGURATION_KEY_DEF.PRIMARY_DATABASE[len(DY_CONFIGURATION_KEY_DEF.DATABASE)+1:]
    return NamingMgr.get_instance().new_naming(orm_name, id, base_class or IDatabaseTable)

__all__ = ["make_db_declarative"]
