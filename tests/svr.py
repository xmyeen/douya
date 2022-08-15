# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging
from typing import List
from pony.orm import PrimaryKey,Required
from sanic import Blueprint, json, text, Sanic
from libdouya.dataclasses.i.rdb import IDatabaseDeclarative
from libdouya.definations.db import OrmDef
from libdouya.definations.cfg import ConfigerDefs
from libdouya.dataclasses.c.db import Databases
from libdouya.core.mgr import ConfigurationMgr
from libdouya.core.deco import obj_d
# from libdouya.serve.dy_server import DyServer
from libdouya.core.hook.db import make_db_declarative
from libdouya.core.app import DyApplication
from libdouya.core.hook.err import mkerr
import libdouya.core.rdb.orm.pony_database
from libdouya.implements.services.sanic_service import SanicAsyncService, BaseAsyncService
import libdouya.implements.configers.default_service_configer
import libdouya.implements.configers.default_database_configer

db_declarative = make_db_declarative(OrmDef.PONY_ORM.value)

class User(db_declarative.table):
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

bp0 = Blueprint.group(bp, url_prefix="/api")

# @app.on_request
# async def run_before_handler(request):
#     request.ctx.user = await fetch_user_by_token(request.token)

@obj_d('httpd')
class MySanicAsyncService(SanicAsyncService):
    def __init__(self):
        SanicAsyncService.__init__(self)
        self.__blueprint = bp0

    def get_blueprint(self) -> Blueprint:
        return self.__blueprint

    async def initialize(self):
        print('Make errr', mkerr(1, "My Error"))

        with self.databases.db().on_transactional_session() as _:
            User(name = '张三', age = 18)

        # self.sanic.ctx.dbs = dbs

@obj_d('cron')
class MyCronAsyncService(BaseAsyncService):
    def __init__(self):
        BaseAsyncService.__init__(self)

    async def initialize(self):
        pass

    async def serve(self): print('Hi,Cron!')

class MyDyApp(DyApplication):
    def __init__(self):
        DyApplication.__init__(self)

    def get_configurations(self) -> List[str]:
        return [
            dict(
                db = dict (
                    priv = dict(url = "sqlite:///app.db")
                ),
                srv = dict(
                    cron = dict(disable = False, schedule = dict( cron = "* * * * * 0/10"), parallel_number = 3),
                    httpd =  dict(parallel_mode = 'mp', disable = False)
                )
            )
        ]

    def get_database_declaratives(self) -> List[IDatabaseDeclarative]:
        return [ db_declarative ]

app = MyDyApp()
app()