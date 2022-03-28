# -*- coding:utf-8 -*-
#!/usr/bin/env Python

import asyncio, asyncio.exceptions, threading, logging, time
from croniter import croniter
from ...dataclasses.c.svr.base_server import BaseAsyncService
from ...dataclasses.c.concurrency.sleeper import Sleeper
from .dy_service_base_executive_worker import IDyServiceBaseExecutiveWorker

class DyServiceThreadExecutiveWorker(IDyServiceBaseExecutiveWorker):
    def __init__(self, srv: BaseAsyncService):
        IDyServiceBaseExecutiveWorker.__init__(self, srv, threading.Event())
        self.__loop: asyncio.BaseEventLoop = asyncio.new_event_loop()
        self.__cron_sleeper: Sleeper = Sleeper()

    def run(self):
        logging.info(f"Execute '{self.srv.name}' service")
        try:
            # with __pypy__.thread.signals_enabled:

            # signames = ('SIGINT', 'SIGTERM', 'SIGQUIT') if 'nt' != os.name else ('CTRL_C_EVENT')
            # for signame in signames:
            #     loop.add_signal_handler(getattr(signal,signame), functools.partial(self.__terminate_service_gracefully, loop))
            for task in self.walk_service(self.__cron_sleeper):
                self.__loop.run_until_complete(task)
        except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
            pass
        except BaseException as e:
            logging.exception(f"Got '{self.srv.name}' service exception")
        finally:
            self.__loop.close()
            logging.info(f"Exit '{self.srv.name}' service")

    def halt_soon(self):
        # super(DyServiceThreadExecutiveWorker, self).halt_soon()
        if self.__cron_sleeper:
            self.__cron_sleeper.wakeup()

        if self.__loop:
            if tasks := [ task for task in asyncio.all_tasks(self.__loop) if not task.done() ]:
                for task in tasks:
                    if not task.cancel():
                        logging.warn(f"Cancel task '{task.get_name()}' failed")

            self.__loop.call_soon_threadsafe(self.__loop.stop)
