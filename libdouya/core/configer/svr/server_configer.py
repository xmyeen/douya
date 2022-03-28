# -*- coding:utf-8 -*-
#!/usr/bin/env Python

import logging
from typing import List,Dict,Any
from attrbox import AttrDict
from ....definations.cfg import DY_CONFIGURATION_KEY_DEF, ConfigerDefs
from ....dataclasses.c.svr.base_server import BaseAsyncService
from ....serve.dy_server import DyServer
from ...mgr import NamingMgr
from ...deco import configer_d

# try:
#     from  .....serve.httpd.sanic_service import SanicAsyncService
# except:
#     pass

@configer_d(DY_CONFIGURATION_KEY_DEF.SERVICE, ConfigerDefs.SRV.value)
class ServerConfiger(object):
    def __init__(self, cfg:AttrDict, *args:List[Any], **kwargs:Dict[str,Any]):
        self.__cfg = cfg

    def __enter__(self):
        return self

    def __exit__(self,exc_type, exc_val, exc_tb):
        pass

    def create_server(self) -> DyServer:
        svcs = []
        for name, subcfg in self.__cfg.items():
            try:
                srv = NamingMgr.get_instance().new_naming(name, name)
                if not isinstance(srv, BaseAsyncService):
                    raise RuntimeError("Invalid service type")

                srv.configuration.update(subcfg.copy())
                svcs.append(srv)
            except:
                logging.exception(f"Can't create service: {name}")

        return DyServer(*svcs)