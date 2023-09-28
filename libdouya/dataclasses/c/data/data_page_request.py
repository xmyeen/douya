# -*- coding:utf-8 -*-
#!/usr/bin/env python

import math, enum
from dataclasses import dataclass
from typing import Self, Iterable
from ....definations.err import ErrorDefs
from ..err import DyError

FIRST_PAGE_NUMBER_DEF = 1

@enum.unique
class SortDirectionDef(enum.Enum):
    ASC = 1
    DESC = 0

class DataSortableColumn:
    def __init__(self, column_name: str, diretion: int):
        self.__column_name = column_name
        self.__direction = diretion

    @property
    def column_name(self) -> str: return self.__column_name

    @property
    def is_ascending(self) -> bool: return self.__direction == SortDirectionDef.ASC.value 

    @property
    def is_descending(self) -> bool: return self.__direction == SortDirectionDef.DESC.value 

    @staticmethod
    def of_asc(column_name: str) -> 'DataSortableColumn':
        return DataSortableColumn(column_name, SortDirectionDef.ASC.value)
    
    @staticmethod
    def of_desc(column_name: str) -> 'DataSortableColumn':
        return DataSortableColumn(column_name, SortDirectionDef.DESC.value)

class DataPageRequest(object):
    def __init__(self, page_number: int, page_size: int, *sortable_columns: DataSortableColumn):
        self.__page_number = page_number
        self.__page_size = page_size
        self.__sortable_columns = list(sortable_columns)

    @staticmethod
    def check_page_parameter_and_get(page_number:int, page_size:int) -> tuple[int,int]:
        if 0 >= page_number:
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make page request failed", error_message = "Invalid 'page_number' parameter", page_number = page_number).as_exception()
        
        if 0 >= page_size: 
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make page request failed", error_message = "Invalid 'page_size' parameter", page_size = page_size).as_exception()
        
        return page_number, page_size

    @staticmethod
    def check_offset_to_page_parameter(offset:int, limit:int) -> tuple[int,int]:
        if 0 > offset:
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make page request failed", error_message = "Invalid 'offset' parameter", offset = offset).as_exception()
        
        if 0 >= limit: 
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make page request failed", error_message = "Invalid 'limit' parameter", limit = limit).as_exception()
        
        n = offset / limit
        pn = math.floor(n)
        if n != pn:
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make page request failed", error_message = "The remainder of 'offset' mod 'limit' isn't equal to zero", limit = limit).as_exception()
        
        return pn, limit
    
    @staticmethod
    def first_page_number() -> int:
        return FIRST_PAGE_NUMBER_DEF
    
    @staticmethod
    def last_page_number(page_size:int, total_size:int) -> int:
        if 0 > total_size:
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make page request failed", error_message = "Invalid 'total_size' parameter", page_size = page_size).as_exception()
        
        if 0 >= page_size: 
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make page request failed", error_message = "Invalid 'page_size' parameter", page_size = page_size).as_exception()
        
        return FIRST_PAGE_NUMBER_DEF if 0 == total_size else math.ceil(total_size / page_size) 

    @staticmethod
    def of(page_number:int, page_size:int, *sortable_columns: DataSortableColumn) -> 'DataPageRequest':
        pn, ps = DataPageRequest.check_page_parameter_and_get(page_number, page_size)
        return DataPageRequest(pn, ps, *sortable_columns)
    
    @staticmethod
    def of_offset(offset:int, limit:int, *sortable_columns: DataSortableColumn) -> 'DataPageRequest':
        pn, ps = DataPageRequest.check_offset_to_page_parameter(offset, limit)
        return DataPageRequest(pn, ps, *sortable_columns)
    
    @property
    def page_number(self) -> int: return self.__page_number
    
    @property
    def page_size(self) -> int: return self.__page_size

    @property
    def offset(self) -> int: return (self.__page_number - 1) * self.__page_size

    def first(self) -> Self:
        pn = self.first_page_number()
        return DataPageRequest(pn, self.__page_size, *self.__sortable_columns)
    
    def last(self, total_size:int) -> Self:
        pn = self.last_page_number(self.__page_size, total_size)
        return DataPageRequest(pn, self.__page_size, *self.__sortable_columns)

    def previous(self) -> Self:
        pn,ps = self.check_page_parameter_and_get(self.__page_number - 1, self.__page_size)
        return DataPageRequest(pn, ps, *self.__sortable_columns)
    
    def next(self) -> Self:
        pn,ps = self.check_page_parameter_and_get(self.__page_number + 1, self.__page_size)
        return DataPageRequest(pn, ps, *self.__sortable_columns)
    
    def previous_or_first(self) -> Self:
        if self.first_page_number() == self.__page_number:
            return self
        else:
            return self.previous() 
        
    def next_or_last(self, total_size:int) -> Self:
        if self.last_page_number(self.__page_size, total_size) == self.__page_number:
            return self
        else:
            return self.next() 
        
    def every_sortable_columns(self) -> Iterable[DataSortableColumn]:
        yield from self.__sortable_columns

    def add_sortable_columns(self, *sortable_columns):
        self.__sortable_columns.extend(sortable_columns)