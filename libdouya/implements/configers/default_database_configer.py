# -*- coding:utf-8 -*-
#!/usr/bin/env python

import logging
from ...definations.cfg import DY_CONFIGURATION_KEY_DEF, ConfigerDefs
from ...dataclasses.i.rdb import IDatabaseDeclarative, IDatabases
from ...dataclasses.c.cfg import DatabaseConfiger
from ...dataclasses.c.db import Databases
from ...core.deco import configer_d

@configer_d(DY_CONFIGURATION_KEY_DEF.DATABASE, ConfigerDefs.DB.value)
class DefaultDatabaseConfiger(DatabaseConfiger):
    def __init__(self):
        DatabaseConfiger.__init__(self)

    async def do_initialization(self, databases: IDatabases):
        for code_name in databases.code_names:
            database = databases.db(code_name)
            await database.initialize()

    async def establish_connection(self, databases: IDatabases):
        for code_name in databases.code_names:
            database = databases.db(code_name)
            await database.establish_connection()

    def get_databases(self, *declaratives:IDatabaseDeclarative) -> IDatabases|None:
        dbs = []
        for declarative in declaratives:
            subcfg = self.configuration.get(declarative.code_name)
            if not subcfg or subcfg.get("disable"): return

            db = declarative.make_proxy(**subcfg)

            try:
                dbs.append(db)
            except:
                logging.exception(f"Initialize database failed: {db.code_name}")

        return Databases(*dbs)