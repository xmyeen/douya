# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging
from typing import List,Dict,Any#,Union
from attrbox import AttrDict
from ....definations.cfg import DY_CONFIGURATION_KEY_DEF, ConfigerDefs
# from ....dataclasses.i.rdb import IDatabase
from ....dataclasses.i.cfg import IDatabaseConfiger
from ....dataclasses.c.db import Databases
from ...deco import configer_d

@configer_d(DY_CONFIGURATION_KEY_DEF.DATABASE, ConfigerDefs.DB.value)
class DatabaseConfiger(IDatabaseConfiger):
    def __init__(self, cfg:AttrDict, *args:List[Any], **kwargs:Dict[str,Any]):
        IDatabaseConfiger.__init__(self)
        self.__cfg = cfg

    def __enter__(self):
        return self

    def init_db(self, databases: Databases):
        for name, subcfg in self.__cfg.items():
            if not subcfg: continue

            try:
                db = databases.db(name)
                if not db: continue
                db.init(**subcfg)
            except:
                logging.exception(f"Initialize failed: {name}")

    def __exit__(self,exc_type, exc_val, exc_tb):
        pass