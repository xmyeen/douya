# -*- coding:utf-8 -*-
#!/usr/bin/env python

from dataclasses import dataclass, asdict
from typing import Self,Any
from ....definations.err import ErrorDefs
from ..err import DyError

@dataclass
class Statusdata(object):
    id: int
    prompt_message: str|None = None
    message: str|None = None

    @classmethod
    def of_dict(cls, data:dict[str, Any]) -> Self:
        id_data = data.get('id')
        if not id_data:
            raise DyError(ErrorDefs.ARG_VALIDATION_FAILED.value, title = "Make status failed", error_message = "Miss 'id' parameter").as_exception()

        return Statusdata(
            id = id_data,
            prompt_message = data.get('prompt_message'),
            message = data.get('message')
        )

    @classmethod
    def of_dict_or(cls, data:dict[str, Any], other: Self | None = None) -> Self | None:
        try:
            return Statusdata.of_dict(data)
        except:
            return other
        
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)