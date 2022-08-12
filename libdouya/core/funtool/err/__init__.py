# -*- coding:utf-8 -*-
#!/usr/bin/env python

# from ...dataclasses.c.err import ErrorDefs, DyError

from typing import Union, Any
from ....dataclasses.c.err import ErrorDefs, DyError
from ...err import ErrorCache
from ...mgr import NamingMgr

def mkerr(id: Union[int, ErrorDefs], *error_messages: Any, **keyword_argument: Any) -> DyError:
    error_cache = NamingMgr.get_instance().new_naming(ErrorCache)
    return error_cache.make_an_error(id, *error_messages, **keyword_argument)