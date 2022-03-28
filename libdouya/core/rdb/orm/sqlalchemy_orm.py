# -*- coding:utf-8 -*-
#!/usr/bin/env Python

from urllib.parse import urlparse
from typing import Any,Dict
try:
    from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
    from sqlalchemy.orm import Session,sessionmaker,scoped_session
    from sqlalchemy.engine import Engine
    from sqlalchemy import create_engine
except:
    pass
from ....definations.db import DialectDef, OptDef, OrmDef
from ....dataclasses.i.rdb import IDatabase
from ...deco import obj_d

@obj_d(OrmDef.SQLALCHEMY_ORM.value)
class SqlalchemyDatabase(IDatabase):
    def __init__(self, name:str, configuration: Dict[str,Any] = None):
        IDatabase.__init__(self, name, configuration)
        self.__base  = declarative_base()
        self.__session_factory = None
        self.__engine = None

    def init(self, **configuration: Dict[str,Any]):
        if configuration:
            self.configuration.update(configuration)

        self.__engine = create_engine(self.url)
        self.__base.metadata.drop_all(self.__engine)
        self.__base.metadata.create_all(self.__engine, checkfirst = True)
        # DbBase.metadata.drop_all(self.__engine)
        # DbBase.metadata.create_all(self.__engine, checkfirst = True)

    def get_core(self) -> Engine:
        return self.__engine

    def get_entity(self) -> DeclarativeMeta:
        return self.__base

    def get_session_factory(self) -> sessionmaker:
        if not self.__session_factory:
            self.__session_factory = sessionmaker(bind = self.__engine)
            if self.configuration.get('multi_threading'):
                self.__session_factory = scoped_session(self.__session_factory)
        return self.__session_factory

    def on_session(self) -> Session:
        session_factory = self.get_session_factory()
        return session_factory()

    def commit(self, session:Session):
        session.commit()

    def rollback(self, session:Session):
        session.rollback()
