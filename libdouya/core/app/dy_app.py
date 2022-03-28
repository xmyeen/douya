# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os, sys, logging, getopt
from typing import List
from ...definations.cfg import DY_CONFIGURATION_KEY_DEF, EnvDefs, ConfigerDefs
from ...utilities.tml import TmlUtl
from ...utilities.module import ModuleUtl
from ..mgr import ConfigurationMgr
from ..configer.svr.server_configer import *

class DyApp(object):
    def __init__(self, *app_modules:str):
        self.__app_module_set = set([ m for m in app_modules if m])
        self.__env = None
        self.__env_configurations = []
        self.__configurations = []

    def __call__(self):
        self.parse_cmdline()

        self.__app_module_set.update([ m for m in os.environ.get(EnvDefs.APP_MODULE.name, "").split(":") if m ])
        if not self.__app_module_set:
            ModuleUtl.import_module(*list(self.__app_module_set))

        ConfigurationMgr.get_instance().init(self.env, *self.get_env_configurations())
        for c in self.get_configurations():
            ConfigurationMgr.get_instance().merge_configuration(c)

        if log_conf := ConfigurationMgr.get_instance().get_conf(DY_CONFIGURATION_KEY_DEF.LOGGER):
            logging.config.dictConfig(log_conf)
        else:
            logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

        svr = None
        with ConfigurationMgr.get_instance().get_configer(ConfigerDefs.SRV.value) as c:
            svr = c.create_server()
        if not svr:
            raise RuntimeError("Create server failed")

        logging.info("Startup application")
        svr.run()
        logging.info("Shutdown application")

    @property
    def exe(self) -> str: return f'{sys.argv[0]}' 

    def get_env(self) -> str: return self.__env
    def set_env(self, env:str): self.__env = env
    env = property(get_env, None, None, "环境")

    def get_usage(self) -> List[str]: return f'{self.exe}'
    # usage = property(get_usage, None, None, "使用说明")

    def get_env_configurations(self) -> List[str]: return self.__env_configurations
    # env_configurations = property(get_env_configurations, None, None, "环境配置")

    def get_configurations(self) -> List[str]: return self.__configurations
    # configurations = property(get_configurations, None, None, "配置")

    def parse_cmdline(self):
        opts, *_ = getopt.getopt(sys.argv[1:], "hc:", ["help", "env=", "configuration-file=", "env-configuration-file="])
        for name, value in opts:
            if name in [ "-h", "--help"]:
                print(self.usage)
                sys.exit(0)
            elif name in [ "--env" ]:
                self.env = value
            elif name in ["-c", "--configuration-file"]:
                self.get_configurations().append(TmlUtl.load(value))
            elif name in ["-c", "--env-configuration-file"]:
                with open(value, 'r', encoding='utf-8') as f:
                    self.get_env_configurations().append(f.read())
