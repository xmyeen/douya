# -*- coding:utf-8 -*-
#!/usr/bin/env python

import types, socket, os
from typing import Any, Coroutine
from sanic import Sanic
from sanic.blueprint_group import BlueprintGroup
from ...dataclasses.c.srv import BaseAsyncService

class SanicAsyncService(BaseAsyncService):
    def __init__(self):
        BaseAsyncService.__init__(self)
        self.__sanic = None

    def __establish_sanic_instance(self):
        if self.__sanic is None:
            self.__sanic = Sanic(
                self.code or 'MySanic',  
                configure_logging = False, 
                ctx = types.SimpleNamespace(databases = self.databases)
            )

            # self.__core.middleware('request')(self.put_context_in_every_request())
            #根据配置生成数据库链接
            #self.db_pool.init_db()

        return self.__sanic

    @property
    def sanic(self) -> Sanic:
        return self.__establish_sanic_instance()

    def get_blueprint(self) -> BlueprintGroup | None: 
        '''蓝图
        '''

    async def serve(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if 'nt' != os.name:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            sock.bind((self.configuration.get('host'), self.configuration.get('port')))
            sock.listen(self.parallel_number)
        else:
            sock.bind((self.configuration.get('host'), self.configuration.get('port')))

        sanic_configuration = dict(
            host = self.configuration.get('host'),
            port = self.configuration.get('port'),
            debug = self.configuration.get('debug'),
            return_asyncio_server = True
        )

        if blueprint := self.get_blueprint():
            self.sanic.blueprint(blueprint)

        svr = await self.sanic.create_server(sock = sock, **sanic_configuration)
        if not svr: raise RuntimeError("Create server failed")
        
        await svr.startup()    
        await svr.serve_forever() # type: ignore
    
        # await self.__core.run(**self.configuration)