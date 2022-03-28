# -*- coding:utf-8 -*-
#!/usr/bin/env Python

import logging, signal, threading, multiprocessing
from dataclasses import dataclass
from asyncio.exceptions import CancelledError
from typing import Any,Union
from ..dataclasses.c.svr.base_server import BaseAsyncService
from .service_executive_worker import IDyServiceBaseExecutiveWorker, DyServiceThreadExecutiveWorker, DyServiceProcessExecutiveWorker

@dataclass
class DyExecutiveWorkerContext:
    worker: IDyServiceBaseExecutiveWorker
    handler: Union[threading.Thread, multiprocessing.Process]

class DyServer(object):
    def __init__(self,  *srvs: BaseAsyncService, **kwargs:Any):
        self.__srvs = srvs

    def __stop_worker(self, *executive_worker_contexts: DyExecutiveWorkerContext):
        #pthread_kill
        for executive_worker_context in executive_worker_contexts:
            executive_worker_context.worker.halt(executive_worker_context.handler)
        for executive_worker_context in executive_worker_contexts:
            executive_worker_context.handler.join()

    def run(self):
        # def signal_handler(signum, frame):
        #     print("1"*30)
        #     self.__exiting_flag.set()
        # signal.signal(signal.SIGTERM, functools.partial(lambda flag: flag.set(), self.__exiting_flag))
        #程序结束信号
        # signal.signal(signal.SIGTERM, signal_handler)
        #监听LINUX的程序打断(interrupt)信号，通是CTLR-C
        # signal.signal(signal.SIGINT, signal_handler)

        # 将多线程和多进程的服务进行分组
        executive_worker_contexts  = []
        for srv in self.__srvs:
            for _ in range(srv.worker_number):
                if srv.parallel_as == 'mp':
                    worker = DyServiceProcessExecutiveWorker(srv)
                    p = multiprocessing.Process(target = DyServiceProcessExecutiveWorker.run, name = srv.name, args = (worker, ))
                    p.start()
                    executive_worker_contexts.append(DyExecutiveWorkerContext(worker = worker, handler = p))
                else:
                    worker = DyServiceThreadExecutiveWorker(srv)
                    t = threading.Thread(target = worker.run, name = srv.name)
                    t.start()
                    executive_worker_contexts.append(DyExecutiveWorkerContext(worker = worker, handler = t))

        try:
            signal.pause()
        except (KeyboardInterrupt, CancelledError):
            pass

        self.__stop_worker(*executive_worker_contexts)

        # for future in concurrent.futures.as_completed(futures_buffer):
        #     try:
        #         res = future.result()
        #     except (KeyboardInterrupt, CancelledError):
        #         print('1'*30)
        #         if mp_pool:
        #             for pid in mp_pool._processes:
        #                 os.kill(pid, signal.SIGKILL)
        #         if mt_pool:
        #             mt_pool.shutdown(wait = True)
        #     except Exception:
        #         logging.exception("Got exception")

        logging.info("Exit all")