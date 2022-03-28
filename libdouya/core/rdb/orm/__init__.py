# -*- coding:utf-8 -*-
#!/usr/bin/env Python

from typing import Dict,Any
from ....dataclasses.i.rdb import IDatabase
from ....definations.cfg import DY_CONFIGURATION_KEY_DEF
from ...mgr import NamingMgr

def mkdb(orm_name:str, name: str = None, configuration: Dict[str,Any] = None) -> IDatabase:
    if not name: name = DY_CONFIGURATION_KEY_DEF.PRIMARY_DATABASE[len(DY_CONFIGURATION_KEY_DEF.DATABASE)+1:]
    return NamingMgr.get_instance().new_naming(orm_name, name, configuration)

__all__ = ["mkdb"]
