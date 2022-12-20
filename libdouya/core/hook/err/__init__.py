# -*- coding:utf-8 -*-
#!/usr/bin/env python

# from ...dataclasses.c.err import ErrorDefs, DyError

from typing import Union, Any
from ....definations.datacache import DatacacheIdDef
from ....dataclasses.c.err import ErrorDefs, DyError, DyException
from ...mgr import DatacacheMgr
from ...mgr.datacache.error import ErrorDatacacheObjectBuilder

def mkerr(id: Union[int, ErrorDefs], *error_messages: Any, **keyword_argument: Any) -> DyError:
    builder = DatacacheMgr \
        .get_instance() \
        .make_builder(DatacacheIdDef.ERROR.value,id)
    
    if not isinstance(builder, ErrorDatacacheObjectBuilder):
        raise RuntimeError(' - '.join([ str(em) for em in error_messages]))

    return builder \
        .and_other_error_messages([ str(em) for em in error_messages ]) \
        .and_keyword_argument(keyword_argument) \
        .build()

def mkex(id: Union[int, ErrorDefs], *error_messages: Any, **keyword_argument: Any) -> DyException:
    return mkerr(id, *error_messages, **keyword_argument).as_exception()