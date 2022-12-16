# -*- coding:utf-8 -*-
#!/usr/bin/env python

from dataclasses import dataclass
from typing import Any,Self
from ....definations.err import ErrorDefs
from ..err import DyError

@dataclass
class Pagination:
    offset: int
    limit: int
    total: int

    @staticmethod
    def from_dict(data:dict[str, Any]) -> Self | None:
        if not data: return None
        
        offset_data = data.get('offset')
        if not offset_data: return None

        limit_data = data.get('limit')
        if not limit_data: return None

        total_data = data.get('total')
        if not total_data: return None

        return Pagination(
            offset = offset_data,
            limit = limit_data,
            total = total_data
        )

    @staticmethod
    def from_page(page_number:int, page_size:int, total_size:int = -1) -> Self:
        if 0 >= page_number: 
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make response failed", error_message = "Miss 'page_number' parameter", page_number = page_number).as_exception()
        
        if 0 > page_size: 
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make response failed", error_message = "Miss 'page_size' parameter", page_size = page_size).as_exception()
        
        if -1 > total_size: 
            total_size = -1
        
        return Pagination(offset = (page_number - 1) * page_size, limit =  page_size, total = total_size)