# -*- coding:utf-8 -*-
#!/usr/bin/env Python

from dataclasses import dataclass
from typing import Any,Dict
from ....definations.err import ErrorDefs
# from ..c.err import DyError
from .pagination import Pagination

@dataclass
class Metadata(object):
    seq: str = None
    pagination: Pagination = None
    passback: Dict[str, Any] = None
    forwared_for: str = None
    track_service_url: str = None