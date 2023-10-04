# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import mapped_column, Mapped
from sanic import Blueprint, json, text, Sanic
from sanic.blueprint_group import BlueprintGroup
from libdouya.dataclasses.i.rdb import IDatabaseDeclarative, IDatabaseProxy
from libdouya.definations.db import OrmDef
from libdouya.definations.cfg import ConfigerDefs
from libdouya.dataclasses.c.db import Databases
from libdouya.core.mgr import ConfigurationMgr
from libdouya.core.deco import obj_d
# from libdouya.serve.dy_server import DyServer
from libdouya.core.hook.db import make_db_declarative
from libdouya.core.app import DyApplication
from libdouya.core.hook.err import mkerr
import libdouya.core.rdb.orm.sqlalchemy_database
from libdouya.implements.services.sanic_service import SanicAsyncService, BaseAsyncService
import libdouya.implements.configers.default_service_configer
import libdouya.implements.configers.default_database_configer

primary_db_declarative = make_db_declarative(OrmDef.SQLALCHEMY_ORM.value)

class User(primary_db_declarative.table):
    __tablename__ = 'sa_user_tbl'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    age:  Mapped[int]

# logging.basicConfig(level = logging.DEBUG)

bp = Blueprint("hi", url_prefix='/hi')

@bp.get('/', version = 1)
async def hi(request,*args, **kwargs):
    sanic = Sanic.get_app('httpd')
    datas = []

    async with sanic.ctx.databases.db().on_session() as session:
        datas.extend([ o.to_dict() for o in await session.scalars(select(User)) ])
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

    def get_blueprint(self) -> BlueprintGroup:
        return self.__blueprint

    async def initialize(self):
        print('Make errr', mkerr(1, "My Error"))

        # if declaratives := self.get_database_declaratives():
        with ConfigurationMgr.get_instance().get_configer(ConfigerDefs.DB.value) as database_configer:
            self.databases = database_configer.get_databases(primary_db_declarative)
            await database_configer.establish_connection(self.databases)

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

    async def initialize(self):
        with ConfigurationMgr.get_instance().get_configer(ConfigerDefs.DB.value) as database_configer:
            databases = database_configer.get_databases(primary_db_declarative)
            await database_configer.do_initialization(databases)
            async with databases.db().on_transactional_session() as session:
                session.add(User(name = '张三', age = 18))

    def get_configurations(self) -> list[dict[str, Any]]:
        return [
            dict(
                db = dict (
                    priv = dict(url = "sqlite+aiosqlite:///app.db")
                ),
                srv = dict(
                    cron = dict(disable = False, schedule = dict( cron = "* * * * * 0/10"), parallel_number = 3),
                    httpd =  dict(parallel_mode = 'mp', disable = False)
                )
            )
        ]

app = MyDyApp()
app()