# -*- coding:utf-8 -*-
#!/usr/bin/env python

from dataclasses import dataclass
from typing import Any,Self
from ....definations.err import ErrorDefs
# from ..c.err import DyError
from .pagination import Pagination

@dataclass
class Metadata(object):
    seq: str|None = None
    pagination: Pagination|None = None
    passback: dict[str, Any]|None = None
    forwared_for: str|None = None
    track_service_url: str|None = None

    @staticmethod
    def of_dict(data:dict[str, Any]) -> 'Metadata':
        return Metadata(
            seq = data.get('seq'),
            pagination = Pagination.of_dict_or(data.get('pagination') or {}),
            passback = data.get('passback'),
            forwared_for = data.get('forwared_for'),
            track_service_url = data.get('track_service_url')
        )
        
