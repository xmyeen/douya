# -*- coding:utf-8 -*-
#!/usr/bin/env python

from sre_constants import SUCCESS
import typing, logging
from ...definations.err import ErrorDefs
from ...dataclasses.c.err import DyError
from ...utilities.tml import TmlUtl
from ..mgr import ConfigurationMgr
from ..deco.naming import svc_d

@svc_d()
class ErrorCache(object):
    def __init__(self):
        self.__default_language = None
        self.__error_entries = {}

    def load(self, **configuration: typing.Any):
        try:
            for error_data_file in  ConfigurationMgr.get_instance().walk_appenv_files("errcfg.toml"):
                err_configuration = TmlUtl.load(error_data_file)
                logging.debug(f"Load error configuration: {err_configuration}")

                self.__default_language = err_configuration.get("default", {}).get("lan")
                for entry in err_configuration.get("entries", []):
                    if not entry: continue
                    for k, v in entry.items():
                        self.__error_entries.update({ k : v })
        except:
            logging.exception("Got an exception")

    def make_an_error(self, id: typing.Union[int, ErrorDefs], *error_messages:typing.Any, **keyword_argument:typing.Any) -> DyError:
        error_id = int(id.value if isinstance(id, ErrorDefs) else id)
        is_successful = ErrorDefs.SUCCESS.value == error_id

        lan_entry = self.__error_entries.get(str(error_id))
        if not lan_entry:
            if substitute_lan_entry := self.__error_entries.get(str(ErrorDefs.SUCCESS.value if is_successful else ErrorDefs.FAILED.value)):
                lan_entry = substitute_lan_entry
            # else:
            #     lan_entry = {}

        entry = lan_entry.get(self.__default_language or "en")
        if not entry:
            entry.setdefault("title", "SUCCESS" if is_successful else "FAILED")
            entry.setdefault("error_message", "SUCCESS" if is_successful else "FAILED")
            entry.setdefault("prompt_message", "SUCCESS" if is_successful else "FAILED")

        dy_error =  DyError(error_id, entry.get("title"), entry.get("error_message"), entry.get("prompt_message"), **keyword_argument)
        if error_messages: dy_error.append(*error_messages)
        return dy_error