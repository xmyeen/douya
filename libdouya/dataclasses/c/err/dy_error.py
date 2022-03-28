# -*- coding:utf-8 -*-
#!/usr/bin/env Python

"""
    dy_error.py - 错误的传递类
"""

from ....definations.err import ErrorDefs
from ...i.err import IDyError
from .dy_exception import DyException

class DyError(IDyError):
    def __init__(self, id:int, title:str = None, message:str = None, prompt_messsage:str = None, **kvs):
        self.__id = id
        self.__title = title
        self.__messages = [message]
        self.__prompt_messsages = [prompt_messsage or message]
        self.__kvs = kvs

    def __repr__(self) -> str:
        return f'Errorcode(id={self.__id}, title={self.__title}, messages={self.__messages}, prompt_messsages={self.__prompt_messsages}, kv={self.__kvs})'

    def __str__(self) -> str:
        return "[0x%x] %s - %s" % (self.id, self.message, ''.join([f'({k} => {v})' for k, v in self.__kvs.items()]))

    def __add__(self, other_error_message) -> 'DyError':
        return self.append(other_error_message)

    def get_id(self)->int: return self.__id
    id = property(get_id, None, None, "编号")

    def get_code(self)->str: return "0x%x"%(self.__id)
    code = property(get_code, None, None, "编码")

    def get_title(self)->str: return self.__title
    title = property(get_title, None, None, "标题")

    def get_message(self)->str: return '. '.join([ m.format(**self.__kvs) for m in self.__messages if m ])
    message = property(get_message, None, None, "消息")

    def get_prompt_messsage(self)->str: return '. '.join([ m.format(**self.__kvs) for m in self.__prompt_messsages if m ])
    prompt_messsage = property(get_prompt_messsage, None, None, "提示")

    def get_curr_message(self)->str: return self.__messages[0] and self.__messages[0].format(**self.__kvs)
    curr_message = property(get_curr_message, None, None, "当前消息")

    def get_curr_prompt_messsage(self)->str: return self.__prompt_messsages[0] and self.__prompt_messsages[0].format(**self.__kvs)
    curr_prompt_messsage = property(get_curr_prompt_messsage, None, None, "当前提示")

    def is_ok(self) -> bool:
        return 0 == self.__id

    def append(self, *other_error_messages) -> 'DyError':
        if other_error_messages:
            for other_error_message in other_error_messages:
                if isinstance(other_error_message, DyError):
                    self.__messages.append(other_error_message.message)
                    self.__prompt_messsages.append(other_error_message.prompt_messsage)
                else:
                    self.__messages.append(str(other_error_message))
                    self.__prompt_messsages.append(str(other_error_message))

        return self

    def exception(self):
        return DyException(self)
