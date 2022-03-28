# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import ABCMeta, abstractclassmethod
from typing import List

class IDyError(metaclass = ABCMeta):
    @abstractclassmethod
    def get_id(self)->int: pass

    @abstractclassmethod
    def get_code(self)->str: pass

    @abstractclassmethod
    def get_title(self)->str: pass

    @abstractclassmethod
    def get_message(self)->str: pass

    @abstractclassmethod
    def get_prompt_messsage(self)->str: pass

    @abstractclassmethod
    def is_ok(self) -> bool:
        '''返回是否成功
        '''

    @abstractclassmethod
    def append(self, *_:List[str]) -> 'IDyError':
        '''附加其他错误消息
        '''

    @abstractclassmethod
    def exception(self):
        '''抛异常
        '''