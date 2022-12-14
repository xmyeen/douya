# -*- coding:utf-8 -*-
#!/usr/bin/env python

'''
    time_d.py - 计时类
'''

import typing, functools
from timeit import default_timer as timer

F = typing.TypeVar("F", bound = typing.Callable[..., typing.Any])
P = typing.ParamSpec("P")
C = typing.Callable[typing.Concatenate[float, P], typing.Any]

class time_d(object):
    def __init__(self, callback: C|None = None, *args:typing.Any, **kwargs:typing.Any):
        self.__callback = callback
        self.__callback_args = args
        self.__callback_kwargs = kwargs
        self.__start_time: float|None = None
        self.__end_time: float|None = None

    @property
    def seconds(self) -> float:
        if not isinstance(self.__start_time, float) or not isinstance(self.__end_time, float):
            raise RuntimeError("Invalid time format")

        return self.__end_time - self.__start_time

    def dang(self):
        if self.__callback: 
            self.__callback(self.seconds, *self.__callback_args, **self.__callback_kwargs)

    def __enter__(self):
        self.__end_time = self.__start_time = timer()
        return self

    def __exit__(self, *args:typing.Any, **kwargs:typing.Any):
        self.__end_time = timer()
        self.dang()

    def __call__(self, func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            with self:
                ret = func(*args, **kwargs)
                return ret
        return typing.cast(F, wrapper)