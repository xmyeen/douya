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

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def of_dict(data:dict[str, Any]) -> 'Req':
        return Req(
            version = data.get('version', 'v1'),
            metadata = Metadata.of_dict(data.get('metadata') or {}),
            data = data.get('data', {})
        )

    @staticmethod
    def build(data:Any, version:str = "v1", metadata:Metadata|None = None) -> 'Req':
        return Req(
            version = version,
            metadata = metadata,
            data = data
        )

@dataclass
class Res(object):
    version: str = "v1"
    statusdata: Statusdata|None = None
    metadata: Metadata|None = None
    datas: list[Any] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def of_dict(data:dict[str, Any]) -> 'Res':
        return Res(
            version = data.get('version', 'v1'),
            statusdata = Statusdata.of_dict(data.get('statusdata') or {}),
            metadata = Metadata.of_dict(data.get('metadata') or {}),
            datas = data.get('datas') or []
        )

    def copy_metadata(self, metadata:Metadata|None = None):
        if metadata:
            self.metadata = metadata

    def is_ok(self) -> bool:
        return (ErrorDefs.SUCCESS.value == self.statusdata.id) if self.statusdata else False

    @staticmethod
    def success(*datas: Any) -> 'Res':
        return Res (
            version = "v1",
            statusdata = Statusdata(
                id = 0,
                prompt_message = "",
                message = ""
            ),
            datas = list(datas)
        )

    @staticmethod
    def fail(err: IDyError,  *datas: Any) -> 'Res':
        return Res (
            version = "v1",
            statusdata = Statusdata(
                id = err.id,
                prompt_message = err.prompt_message,
                message = str(err)
            ),
            datas = list(datas)
        )


__all__ = [
    "Metadata",
    "Pagination",
    "Statusdata",
    "Req", "Res"
]
