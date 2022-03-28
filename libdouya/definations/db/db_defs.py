# -*- coding:utf-8 -*-
#!/usr/bin/env Python

'''
    db_defs.py - 数据库相关
'''

from enum import Enum,unique

@unique
class DialectDef(Enum):
    SQLITE = "sqlite"
    PG = "postgresql"

@unique
class OptDef(Enum):
    CREATING_TABLES = "creating_tables"
    DROPPING_TABLES = "dropping_tables"

@unique
class OrmDef(Enum):
    PONY_ORM = "orm:pony"
    SQLALCHEMY_ORM = "orm:sqlalchemy"
