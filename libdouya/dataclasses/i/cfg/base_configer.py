# -*- coding:utf-8 -*-
#!/usr/bin/env python

from abc import ABCMeta, abstractproperty, abstractmethod
from attrbox import AttrDict

class IBaseConfiger(metaclass = ABCMeta):
    def __init__(self): pass

    @property
    @abstractmethod
    def configuration(self) -> AttrDict:
        '''配置'''
    @configuration.setter
    def configuration(self, val:AttrDict): pass

    @abstractmethod
    def initialize(self, *args, **kwargs): pass