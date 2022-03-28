# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import ABCMeta, abstractclassmethod
from typing import Any, List, Dict, Union
from ....definations.db import OptDef

class IDatabase(object, metaclass = ABCMeta):
    def __init__(self, name:str, configuration: Dict[str,Any] = None):
        self.__name = name
        self.__configuration  = configuration or {}

    @property
    def name(self) -> str:
        return self.__name

    @property
    def configuration(self) -> Dict[str,Any]:
        return self.__configuration

    @property
    def url(self) -> str:
        '''数据库链接
        形如： dialect+driver://username:password@host:port/database
        '''
        return self.configuration.get('url', "sqlite:///:memory:")

    @property
    def options(self) -> Union[List[str], None]:
        return self.configuration.get('options', [OptDef.CREATING_TABLES.value])

    @property
    def is_debugging(self) -> bool:
        return bool(self.configuration.get('is_debugging', False))

    @property
    def core(self) -> Any:
        return self.get_core()

    @property
    def entity(self) -> Any:
        return self.get_entity()

    @property
    def session(self) -> Any:
        return self.get_session_factory()

    @abstractclassmethod
    def init(self, **configuration: Dict[str,Any]):
        '''需要确保线程可重复
        '''
        pass

    @abstractclassmethod
    def get_core(self) -> Any: pass

    @abstractclassmethod
    def get_entity(self) -> Any: pass

    @abstractclassmethod
    def get_session_factory(self) -> Any: pass

