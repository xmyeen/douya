# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging, os, asyncio
from urllib.parse import urlparse
from typing import Any, AsyncIterable
from contextlib import asynccontextmanager
# from sqlalchemy.orm import declarative_base, DeclarativeMeta
# from sqlalchemy.orm import Session,sessionmaker,scoped_session
# from sqlalchemy.engine import Engine
# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_scoped_session, AsyncSessionTransaction, async_sessionmaker, async_scoped_session
from ....definations.err import ErrorDefs
from ....definations.db import DialectDef, OptDef, OrmDef, OrmConnectionPoolTypeDef
from ....dataclasses.i.rdb import IDatabaseDeclarative, IDatabaseProxy, IDatabaseTable
from ....dataclasses.c.err import DyError
from ...deco import obj_d
from .parent.base_database import BaseDatabaseDeclarative, BaseDatabaseProxy

class SQLAlchemyDatabase(BaseDatabaseProxy):
    def __init__(self, id:str, declarative: IDatabaseDeclarative, **configuration: Any):
        BaseDatabaseProxy.__init__(self, id, declarative, **configuration)
        self.__session_factory = None
        self.__engine = None

    def __make_session(self) -> AsyncSession|async_scoped_session:
        if not self.__session_factory:
            self.__session_factory = async_sessionmaker(bind = self.__engine)
            if self.configuration.get('multi_threading'):
                self.__session_factory = async_scoped_session(self.__session_factory, scopefunc = asyncio.current_task)
        return self.__session_factory()

    @property
    def internal_implementation(self) -> AsyncEngine:
        return self.__engine

    def get_orm_connection_pool_type(self) -> str:
        return OrmConnectionPoolTypeDef.EVERY_PROCESSOR.value

    async def connect(self, enable_scheme_rebuiding:bool):
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
        self.__engine = create_async_engine(
            final_connection_url,
            # pool_size = int(self.configuration.get("pool_size", 10)), #默认是10个
            # pool_recycle = int(self.configuration.get("pool_timeout", -1)), # 默认不回收线程池
            echo = bool(self.configuration.get("echo", False)), # 打印数据库相关
            echo_pool = bool(self.configuration.get("echo", False)) # 打印数据库相关
        )

        async with self.__engine.begin() as conn:
            if enable_scheme_rebuiding:
                if OptDef.DROPPING_TABLES.value in connection_options:
                    await conn.run_sync(self.declarative.table.metadata.drop_all)
                if OptDef.CREATING_TABLES.value in connection_options:
                    await conn.run_sync(self.declarative.table.metadata.create_all, checkfirst = True)
            # DbBase.metadata.drop_all(self.__engine)
            # DbBase.metadata.create_all(self.__engine, checkfirst = True)

    @asynccontextmanager
    async def on_session(self) -> AsyncIterable[AsyncSession|async_scoped_session]:
        session = self.__make_session()
        try:
            yield session
        finally:
            await session.close()

    @asynccontextmanager
    async def on_transactional_session(self) -> AsyncIterable[AsyncSession|async_scoped_session]:
        session = self.__make_session()
        async with session.begin() as transaction:
            try:
                yield session
                await transaction.commit()
            except BaseException as e:
                # logging.exception("Got some exception")
                await transaction.rollback()
                raise DyError(ErrorDefs.DB_OPERATE_FAILED.value, "Operate Database Failed", str(e)).as_exception()
            finally:
                await session.close()

@obj_d(OrmDef.SQLALCHEMY_ORM.value)
class SQLAlchemyDatabaseDeclarative(BaseDatabaseDeclarative):
    def __init__(self, code_name:str, base_class: type[IDatabaseTable]):
        BaseDatabaseDeclarative.__init__(self, code_name)
        # self.__base : DeclarativeMeta  = declarative_base(AsyncAttrs, cls = SQLAlchemyTableBase)
        self.__base_class = base_class

    @property
    def table(self) -> IDatabaseTable:
        return self.__base_class

    def make_proxy(self, **configuration:Any) -> IDatabaseProxy:
        return SQLAlchemyDatabase(self.code_name, self, **configuration)