# -*- coding:utf-8 -*-
#!/usr/bin/env python

from dataclasses import dataclass, asdict
from typing import Any, Self
from ....definations.err import ErrorDefs
from ..err import DyError
from ..data import DataPageRequest

@dataclass
class Pagination:
    offset: int
    limit: int
    total: int

    @classmethod
    def of_dict(cls, data:dict[str, Any]) -> Self:
        offset_data = data.get('offset')
        if not offset_data:
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make pagination failed", error_message = "Miss 'offset' parameter").as_exception()

        limit_data = data.get('limit')
        if not limit_data:
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make pagination failed", error_message = "Miss 'limit' parameter").as_exception()

        total_data = data.get('total')
        if not total_data:
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make pagination failed", error_message = "Miss 'total' parameter").as_exception()

        return Pagination(offset = offset_data, limit = limit_data, total = total_data)

    @classmethod
    def of_dict_or(cls, data:dict[str, Any], other: Self | None = None) -> Self | None:
        try:
            return Pagination.of_dict(data)
        except:
            return other
        
    @classmethod
    def make_of_page(cls, page_number:int, page_size:int, total_size:int = -1) -> Self:
        pn, ps = DataPageRequest.check_page_parameter_and_get(page_number, page_size)
        if -1 > total_size: total_size = -1
        
        return Pagination(offset = (pn - 1) * page_size, limit =  ps, total = total_size)
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
    
    def to_page_request(self) -> DataPageRequest:
        return DataPageRequest.of_offset(self.offset, self.limit)