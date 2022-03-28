# -*- coding:utf-8 -*-
#!/usr/bin/env Python

from dataclasses import dataclass

@dataclass
class Statusdata(object):
    id: int
    message: str
    prompt_message: str = None