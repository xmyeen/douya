# -*- coding:utf-8 -*-
#!/usr/bin/env python

import threading, multiprocessing, asyncio, time
from typing import Union
from abc import ABCMeta, abstractclassmethod
from croniter import croniter
from ...definations.cfg import ConfigerDefs
from ...dataclasses.c.concurrency.sleeper import Sleeper
from ...dataclasses.c.svr.base_server import BaseAsyncService
from ...core.mgr import ConfigurationMgr

class IDyServiceBaseExecutiveWorker(metaclass = ABCMeta):
    def __init__(self, srv: BaseAsyncService, halt_flag: Union[threading.Event, multiprocessing.Event]):
        self.__srv = srv
        self.__halt_flag = halt_flag

    def get_srv(self) -> BaseAsyncService: return self.__srv
    srv = property(get_srv, None, None, '服务')

    def is_running(self) -> bool:
        '''是否运行
        '''
        return not self.__halt_flag.is_set()

    @abstractclassmethod
    def run(self): pass

    @abstractclassmethod
    def halt_soon(self): pass

    def halt(self, handler: Union[threading.Thread, multiprocessing.Process]):
        if not handler.is_alive():
            return

        self.__halt_flag.set()
        self.halt_soon()

        if isinstance(handler, multiprocessing.Process):
            handler.kill()

    def walk_service(self, cron_sleeper: Sleeper) -> asyncio.Task:
        if self.srv.databases:
            with ConfigurationMgr.get_instance().get_configer(ConfigerDefs.DB.value) as cf:
                cf.init_db(self.srv.databases)

        # if t1 is not None and 0 == getattr(t1 - t0, 'seconds'):
        #     t0 = t0 + datetime.timedelta(seconds = 1)
        yield self.srv.init()

        if self.srv.cron_text:
            iter = croniter(self.srv.cron_text)
            while self.is_running():
                t0 = time.time()
                t1 = iter.get_next(float, t0)
                if 1 > t1 - t0:
                    t1 = iter.get_next(float, t1 + 1)
                cron_sleeper.sleep(t1 - t0)
                # loop.run_until_complete(asyncio.sleep(getattr(t1 - t0, 'seconds')))
                yield self.srv.serve()
        else:
            yield self.srv.serve()