# -*- coding:utf-8 -*-
#!/usr/bin/env Python

import os
from urllib.parse import urlparse
from typing import Any,Dict
try:
    from pony.orm import Database as OrmDatabase
    from pony.orm import commit as orm_commit, rollback as orm_rollback
    from pony.orm.core import DBSessionContextManager as OrmSessionContextManager
except:
    pass
from ....definations.db import DialectDef, OptDef, OrmDef
from ....dataclasses.i.rdb import IDatabase
from ...deco import obj_d

@obj_d(OrmDef.PONY_ORM.value)
class PonyDatabase(IDatabase):
    def __init__(self, name:str, configuration: Dict[str,Any] = None):
        IDatabase.__init__(self, name, configuration)
        self.__core = OrmDatabase()
        self.__session_factory = None

    def init(self, **configuration: Dict[str,Any]):
        '''需要确保线程可重复
        '''
        if configuration:
            self.configuration.update(configuration)

        db_options = self.options or []

        u = urlparse(self.url)
        if u.scheme is None:
            raise RuntimeError(f"Invalid database url. No 'scheme' found : {self.url}")
        elif u.scheme.lower() == DialectDef.SQLITE.value.lower():
            if u.path in ['', '/', '/:memory:']:
                self.__core.bind(provider='sqlite', filename = ':memory:')
            else:
                db_dir = self.configuration.get("db_dir", os.getcwd())
                file_name = os.path.join(db_dir, u.path[1:])
                self.__core.bind(provider='sqlite', filename = file_name, create_db = True)
        elif u.scheme.lower() == DialectDef.PG.value.lower():
            # postgresql://scott:tiger@localhost:5432/mydatabase'
            opt = {}
            if u.path in ['', '/']: raise RuntimeError(f"Invalid database url. No 'database' found: {self.url}")
            if u.username: opt.update(user = u.username)
            if u.password: opt.update(password = u.password)
            if u.hostname: opt.update(host = u.hostname)
            if u.port: opt.update(port = u.port)
            # self.__core.bind(provider='postgres', user='testor', password='testor', host='10.19.156.28', port=30432, database='testdb')
            # db.bind(provider='mysql', host='', user='', passwd='', db='')
            # db.bind(provider='oracle', user='', password='', dsn='')
            self.__core.bind(provider='postgres', database=u.path[1:], **opt)
        else:
            raise RuntimeError(f"Unsupported database: {self.url}")

        self.__core.generate_mapping(
            create_tables =  OptDef.CREATING_TABLES.value in db_options
        )

    def get_core(self) -> OrmDatabase:
        return self.__core

    def get_entity(self) -> Any:
        return self.__core.Entity

    def get_session_factory(self) -> OrmSessionContextManager:
        if not self.__session_factory:
            self.__session_factory = OrmSessionContextManager(sql_debug =  self.is_debugging)
        return self.__session_factory

    def on_session(self) -> 'None':
        session_factory = self.get_session_factory()
        return session_factory()

    def commit(self, session:'None'):
        orm_commit()

    def rollback(self, session:'None'):
        orm_rollback()