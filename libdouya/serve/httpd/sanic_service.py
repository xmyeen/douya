# -*- coding:utf-8 -*-
#!/usr/bin/env Python

import types
from sanic import Blueprint,Sanic
from ...dataclasses.c.svr import BaseAsyncService
from ...dataclasses.c.db import Databases

class SanicAsyncService(BaseAsyncService):
    def __init__(self, name:str, dbs:Databases = None):
        BaseAsyncService.__init__(self, name, dbs)
        self.__blueprint = None
        self.__core = Sanic(name,  configure_logging = False, ctx = types.SimpleNamespace(databases = dbs))

    @property
    def sanic(self) -> Sanic: return self.__core

    def get_blueprint(self) -> Blueprint: return self.__blueprint
    def set_blueprint(self, blueprint:Blueprint): self.__blueprint = blueprint
    blueprint = property(get_blueprint, set_blueprint, None, "蓝图")

    async def init(self):
        #根据配置生成数据库链接
        #self.db_pool.init_db()
        pass

    async def serve(self):
        cfg = dict(
            host = self.configuration.get('host'),
            port = self.configuration.get('port'),
            debug = self.configuration.get('debug'),
        )
        cfg.update(return_asyncio_server = True)

        if self.blueprint:
            self.sanic.blueprint(self.blueprint)

        srv = await self.sanic.create_server(**cfg)
        await srv.startup()
        await srv.serve_forever()
        # await self.__core.run(**self.configuration)