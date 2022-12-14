# -*- coding:utf-8 -*-
#!/usr/bin/env python

from typing import Any,Dict,List
from dataclasses import dataclass, field, asdict
from ....definations.err import ErrorDefs
from ..err import DyError
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
    def from_dict(data:dict[str, Any]) -> 'Req' | None:
        if not data: return None
        
        metadata_data = data.get('metadata')
        
        return Req(
            version = data.get('version', 'v1'),
            metadata = metadata_data and Metadata.from_dict(metadata_data),
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
    def from_dict(data:dict[str, Any]) -> 'Res' | None:
        if not data: return None
        
        statusdata_data = data.get('statusdata')
        if statusdata_data is None: return None

        metadata_data = data.get('metadata')

        return Res(
            version = data.get('version', 'v1'),
            statusdata = Statusdata.from_dict(statusdata_data),
            metadata = metadata_data and Metadata.from_dict(metadata_data),
            datas = data.get('datas') or []
        )

    def copy_metadata(self, metadata:Metadata|None = None):
        if metadata:
            self.metadata = metadata

    def is_ok(self) -> bool:
        return (ErrorDefs.SUCCESS.value == self.statusdata.id) if self.statusdata else False

    @staticmethod
    def success(*datas: Any):
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
    def fail(err: DyError,  *datas: Any):
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
