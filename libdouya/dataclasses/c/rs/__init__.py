# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Any,Self
from dataclasses import dataclass, field, asdict
from ....definations.err import ErrorDefs
from ...i.err import IDyError
from .metadata import Metadata
from .pagination import Pagination
from .statusdata import Statusdata

@dataclass
class Req(object):
    version: str = "v1"
    metadata: Metadata|None = None
    data: dict[str,Any] = field(default_factory = dict)

    @classmethod
    def of_dict(cls, data:dict[str, Any]) -> Self:
        return Req(
            version = data.get('version', 'v1'),
            metadata = Metadata.of_dict(data.get('metadata') or {}),
            data = data.get('data', {})
        )

    @classmethod
    def build(cls, data:Any, version:str = "v1", metadata:Metadata|None = None) -> Self:
        return Req(
            version = version,
            metadata = metadata,
            data = data
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
    
    def and_metadata(self, metadata:Metadata) -> Self:
        self.metadata = metadata
        return self

@dataclass
class Res(object):
    version: str = "v1"
    statusdata: Statusdata|None = None
    metadata: Metadata|None = None
    datas: list[Any] = field(default_factory=list)

    @classmethod
    def of_dict(cls, data:dict[str, Any]) -> Self:
        return Res(
            version = data.get('version', 'v1'),
            statusdata = Statusdata.of_dict(data.get('statusdata') or {}),
            metadata = Metadata.of_dict(data.get('metadata') or {}),
            datas = data.get('datas') or []
        )

    @classmethod
    def success(cls, *datas: Any) -> Self:
        return Res (
            version = "v1",
            statusdata = Statusdata(
                id = 0,
                prompt_message = "",
                message = ""
            ),
            datas = list(datas)
        )

    @classmethod
    def fail(cls, err: IDyError,  *datas: Any) -> Self:
        return Res (
            version = "v1",
            statusdata = Statusdata(
                id = err.id,
                prompt_message = err.prompt_message,
                message = str(err)
            ),
            datas = list(datas)
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
    
    def and_status(self, statusdata:Statusdata) -> Self:
        self.statusdata = statusdata
        return self
    
    def and_meta(self, metadata:Metadata) -> Self:
        self.metadata = metadata
        return self

    def is_ok(self) -> bool:
        return (ErrorDefs.SUCCESS.value == self.statusdata.id) if self.statusdata else False


__all__ = [
    "Metadata",
    "Pagination",
    "Statusdata",
    "Req", "Res"
]
