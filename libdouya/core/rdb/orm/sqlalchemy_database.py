# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging, os
from urllib.parse import urlparse
from typing import Any,Dict
from contextlib import contextmanager

try:
    from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
    from sqlalchemy.orm import Session,sessionmaker,scoped_session
    from sqlalchemy.engine import Engine
    from sqlalchemy import create_engine
except:
    pass
from ....definations.err import ErrorDefs
from ....definations.db import DialectDef, OptDef, OrmDef, OrmConnectionPoolTypeDef
from ....dataclasses.i.rdb import IDatabaseDeclarative, IDatabaseProxy
from ....dataclasses.c.err import DyError
from ...deco import obj_d
from .parent.base_database import BaseDatabaseDeclarative, BaseDatabaseProxy

class SQLAlchemyDatabase(BaseDatabaseProxy):
    def __init__(self, id:str, declarative: IDatabaseDeclarative, **configuration: Any):
        BaseDatabaseProxy.__init__(self, id, declarative, **configuration)
        self.__session_factory = None
        self.__engine = None

    def __get_session_factory(self) -> scoped_session | sessionmaker: # pyright: reportUnboundVariable=false
        if not self.__session_factory:
            self.__session_factory = sessionmaker(bind = self.__engine)
            if self.configuration.get('multi_threading'):
                self.__session_factory = scoped_session(self.__session_factory)
        return self.__session_factory

    @property
    def internal_implementation(self) -> Any:
        return self.__engine

    def get_orm_connection_pool_type(self) -> str:
        return OrmConnectionPoolTypeDef.EVERY_PROCESSOR.value

    def connect(self, enable_scheme_rebuiding:bool):
        connection_options = self.connection_options or []

        final_connection_url = self.connection_url

        u = urlparse(self.connection_url)
        if u.scheme is None:
            raise RuntimeError(f"Invalid database url. No 'scheme' found : {self.connection_url}")
        elif u.scheme.lower() == DialectDef.SQLITE.value.lower():
            if u.path not in ['', '/', '/:memory:']:
                if db_dir := self.configuration.get("db_dir"):
                    db_dir_path = db_dir.replace('\\', '/')
                    if not db_dir.startswith('/'): db_dir_path = f'/{db_dir_path}'

                    final_connection_url = self.connection_url.replace(u.path, f'{db_dir_path}{u.path}')

        logging.debug(f"Make engine for database: {final_connection_url}")
        self.__engine = create_engine(
            final_connection_url,
            pool_size = int(self.configuration.get("pool_size", 10)), #默认是10个
            pool_recycle = int(self.configuration.get("pool_timeout", -1)), # 默认不回收线程池
            echo = bool(self.configuration.get("echo", False)), # 打印数据库相关
            echo_pool = bool(self.configuration.get("echo", False)) # 打印数据库相关
        )

        if enable_scheme_rebuiding:
            if OptDef.DROPPING_TABLES.value in connection_options:
                self.declarative.internal_implementation.metadata.drop_all(self.__engine)
            if OptDef.CREATING_TABLES.value in connection_options:
                self.declarative.internal_implementation.metadata.create_all(self.__engine, checkfirst = True)
            # DbBase.metadata.drop_all(self.__engine)
            # DbBase.metadata.create_all(self.__engine, checkfirst = True)

    @contextmanager
    def on_session(self) -> Any:
        session_factory = self.__get_session_factory()
        yield session_factory()

    @contextmanager
    def on_transactional_session(self) -> Any:
        with self.on_session() as s:
            try:
                yield s
                s.commit()
            except BaseException as e:
                # logging.exception("Got some exception")
                s.rollback()
                raise DyError(ErrorDefs.DB_OPERATE_FAILED.value, "Operate Database Failed", str(e)).as_exception()

class SQLAlchemyTableBase(object):
    def __init__(self): pass

    def to_dict(self) -> dict[str, Any]:
        return { c.name : getattr(self, c.name, None) for c in self.__table__.columns } # type: ignore # ignore: type

@obj_d(OrmDef.SQLALCHEMY_ORM.value)
class SQLAlchemyDatabaseDeclarative(BaseDatabaseDeclarative):
    def __init__(self, code_name:str):
        BaseDatabaseDeclarative.__init__(self, code_name)
        self.__base : DeclarativeMeta  = declarative_base(cls = SQLAlchemyTableBase)

    @property
    def table(self) -> Any:
        return self.__base

    @property
    def internal_implementation(self) -> Any:
        return self.__base

    def make_proxy(self, **configuration:Any) -> IDatabaseProxy:
        return SQLAlchemyDatabase(self.code_name, self, **configuration)