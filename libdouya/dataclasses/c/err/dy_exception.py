# -*- coding:utf-8 -*-
#!/usr/bin/env Python

from typing import List
from ...i.err import IDyError

class DyException(Exception):
    def __init__(self, error:IDyError):
        super().__init__(self, error)
        self.__error = error

    def append(self, *msgs:List[str]):
        self.__error.append(*msgs)
        return self

    @property
    def error(self):
        return self.__error