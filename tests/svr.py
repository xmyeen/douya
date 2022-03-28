# -*- coding:utf-8 -*-
#!/usr/bin/env Python

import logging
from typing import List
from pony.orm import PrimaryKey,Required
from sanic import Blueprint, json, text, Sanic
from libdouya.definations.db import OrmDef
from libdouya.definations.cfg import ConfigerDefs
from libdouya.core.mgr.configuration_mgr.configuration_mgr import ConfigurationMgr
from libdouya.dataclasses.c.db import Databases
from libdouya.core.deco import obj_d
# from libdouya.serve.dy_server import DyServer
import libdouya.core.configer.svr.server_configer
import libdouya.core.configer.db.database_configer
from libdouya.core.rdb.orm import mkdb
from libdouya.core.app import DyApp
from libdouya.serve.httpd.sanic_service import SanicAsyncService, BaseAsyncService
import libdouya.core.rdb.orm.pony_orm

db = mkdb(OrmDef.PONY_ORM.value)

class User(db.entity):
    id = PrimaryKey(int, auto = True)
    name = Required(str)
    age = Required(int)

# logging.basicConfig(level = logging.DEBUG)

bp = Blueprint("hi", url_prefix='/hi')
@bp.get('/', version = 1)
def hi(request,*args, **kwargs):
    sanic = Sanic.get_app('httpd')
    datas = []

    with sanic.ctx.databases.db().on_session() as s:
        datas.extend([ o.to_dict() for o in User.select() ])
    # print('1'*30, request, sanic.ctx, args,  kwargs)
    return json(dict(datas = datas), ensure_ascii = False)


# @app.on_request
# async def run_before_handler(request):
#     request.ctx.user = await fetch_user_by_token(request.token)

@obj_d('httpd')
class MySanicAsyncService(SanicAsyncService):
    def __init__(self, name:str):
        SanicAsyncService.__init__(self, name, Databases(db))

    async def init(self):
        self.blueprint = bp

        with self.databases.db().on_session() as s:
            User(name = '张三', age = 18)
            self.databases.db().commit(s)

        # self.sanic.ctx.dbs = dbs

@obj_d('cron')
class MyCronAsyncService(BaseAsyncService):
    def __init__(self, name:str):
        BaseAsyncService.__init__(self, name)

    async def init(self):
        self.blueprint = bp

    async def serve(self): print('Hi,Cron!')

class MyDyApp(DyApp):
    def __init__(self):
        DyApp.__init__(self)

    def get_configurations(self) -> List[str]:
        return [
            dict(srv = dict(
                cron = dict(cron = "* * * * * 0/10", worker_number = 3),
                httpd =  dict(parallel_as = 'mp')
            ))
        ]

app = MyDyApp()
app()