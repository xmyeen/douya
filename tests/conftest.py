# -*- coding:utf-8 -*-
#!/usr/bin/env Python

import os, pytest, tempfile
from libdouya.definations.db import OrmDef
from libdouya.core.mgr import ConfigurationMgr
from libdouya.core.rdb.orm import mkdb
from libdouya.definations.cfg.env_defs import EnvDefs

# @pytest.fixture(autouse=True)
# def run_around_tests():
#     # Code that will run before your test, for example:
#     files_before = # ... do something to check the existing files
#     # A test function will be run at this point
#     yield
#     # Code that will run after your test, for example:
#     files_after = # ... do something to check the existing files
#     assert files_before == files_after
# scope
#   function: 每个函数或方法都会调用
#   class: 每一个类调用一次
#   module: 每一个py文件调用一次，该文件内又有多个function和class
#   session 是多个文件调用一次，可以跨.py文件调用。


@pytest.fixture(scope = 'function')
def make_temp_env_of_app_cfg():
    old_environ = os.environ.copy()
    with tempfile.TemporaryDirectory() as td:
        os.environ.update({
            EnvDefs.APP_CFG_DIR.name : os.path.abspath(td),
            EnvDefs.APP_CFG_NAME.name : f"test.json"
        })
        yield os.environ
    os.environ = old_environ
    
@pytest.fixture(scope = 'function')
def make_temp_env_of_lookup():
    old_environ = os.environ.copy()
    with tempfile.TemporaryDirectory() as td:
        dirnames = [ os.path.join(td, str(i)) for i in range(0, 5) ]
        [ os.makedirs(dirname) for dirname in dirnames ] 
        os.environ.update({ EnvDefs.APP_LOOKUP_DIR.name : ":".join(dirnames) })
        yield os.environ
    os.environ = old_environ

@pytest.fixture(scope = 'function')
def make_db_from_configuration():
    ConfigurationMgr.get_instance().init()
    db = mkdb(OrmDef.PONY_ORM.value)
    yield db
    # print(db.core.close)
    # old_environ = os.environ.copy()
    # with tempfile.TemporaryDirectory() as td:
    #     dirnames = [ os.path.join(td, str(i)) for i in range(0, 5) ]
    #     [ os.makedirs(dirname) for dirname in dirnames ] 
    #     os.environ.update({ EnvDefs.APP_LOOKUP_DIR.name : ":".join(dirnames) })
    #     yield os.environ
    # os.environ = old_environ