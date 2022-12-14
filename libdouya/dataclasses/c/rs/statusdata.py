# -*- coding:utf-8 -*-
#!/usr/bin/env python

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Statusdata(object):
    id: int
    prompt_message: str|None = None
    message: str|None = None

    @staticmethod
    def from_dict(data:dict[str, Any]) -> 'Statusdata' | None:
        if not data: return None

        id_data = data.get('id')
        if not id_data: return None

        return Statusdata(
            id = id_data,
            prompt_message = data.get('prompt_message'),
            message = data.get('message')
        )