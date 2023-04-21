# -*- coding:utf-8 -*-
#!/usr/bin/env python

'''
    text_markup_language_utility.py - 文本标记语言通用方法集
'''

import os, codecs, json, tomllib
from typing import Any
from pathlib import Path
from dataclasses import dataclass
from attrbox import AttrDict, AttrList

try:
    import yaml
except:
    yaml = None

from ...definations.tml import TmlDefs
from ...dataclasses.c.err import ErrorDefs,DyError

@dataclass
class TmlConf(object):
    lan: TmlDefs
    file_ext_names: list[str]

class TmlUtl(object):
    @staticmethod
    def walk_conf():
        for _, en in TmlDefs.__members__.items():
            yield TmlConf(lan = en, file_ext_names = [ nm.lower() for nm in en.value.split(":") if nm ])

    @staticmethod
    def guess_file(file_path_like: Path|str) -> TmlDefs|None:
        file_path = Path(file_path_like) if isinstance(file_path_like, str) else file_path_like

        if file_path.suffix:
            for tml_conf in TmlUtl.walk_conf():
                if file_path.suffix[1:].lower() in tml_conf.file_ext_names:
                    return tml_conf.lan

        return None

    @staticmethod
    def suffix_extend_names(file_basename:str, *lans:TmlDefs) -> list[str]:
        file_names = []
        for tml_conf in TmlUtl.walk_conf():
            if tml_conf.lan in lans:
                file_names.extend([ f"{file_basename}.{file_ext_name}" for file_ext_name in tml_conf.file_ext_names ])
        return file_names

    @staticmethod
    def loads(text: str, lan:TmlDefs, input_encoding:str|None = None, *args, **kwargs) -> list|dict:
        if text is None:
            raise DyError(ErrorDefs.ARGS_MUSTBE_EXIST.value, title = "No argument exist", error_message = "Miss 'text' argument").as_exception()
        if lan is None:
            raise DyError(ErrorDefs.ARGS_MUSTBE_EXIST.value, title = "No argument exist", error_message = "Miss 'lan' argument").as_exception()

        if not input_encoding: input_encoding = 'utf-8'
        input_str = text.encode(input_encoding).decode('utf-8') if 'utf-8' != codecs.lookup(input_encoding).name else text

        if TmlDefs.JSON == lan:
            return json.loads(input_str, *args, **kwargs)
        elif TmlDefs.TOML == lan:
            return tomllib.loads(input_str)
        elif TmlDefs.YAML == lan:
            if yaml is None:
                raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", error_message = "Can't import 'yaml' module").as_exception()
            return yaml.load(input_str, Loader = yaml.Loader)
        else:
            raise DyError(ErrorDefs.UNSUPPORTED_CONFIGURATION_FORMAT.value, title = "Unsupport", error_message = f"Unsupported configuration format: {lan or 'None'}").as_exception()

    @staticmethod
    def loads_attr(text: str, lan:TmlDefs, input_encoding:str|None = None, *args, **kwargs) -> AttrDict|AttrList:
        rv = TmlUtl.loads(text, lan, input_encoding, *args, **kwargs)
        return AttrList(rv) if isinstance(rv, list) else AttrDict(rv)

    @staticmethod
    def dumps(obj: dict, lan:TmlDefs, *args, **kwargs) -> str:
        if obj is None:
            raise DyError(ErrorDefs.ARGS_MUSTBE_EXIST.value, title = "No argument exist", error_message = "Miss 'obj' argument").as_exception()
        if lan is None:
            raise DyError(ErrorDefs.ARGS_MUSTBE_EXIST.value, title = "No argument exist", error_message = "Miss 'lan' argument").as_exception()

        output_str: str|None = None

        match lan:
            case TmlDefs.JSON:
                output_str = json.dumps(obj, *args, **kwargs)
            case TmlDefs.TOML:
                raise DyError(ErrorDefs.UNSUPPORTED.value, title = "Unsuppoted", error_message = "Unsuppot dump").as_exception()
            case TmlDefs.YAML:
                if yaml is None:
                    raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", error_message = "Can't import 'yaml' module").as_exception()
                # ef = codecs.EncodedFile(bio, "utf-8", output_encoding or 'utf-8')
                output_str = yaml.dump(obj, *args, **kwargs)
            case _:
                raise DyError(ErrorDefs.UNSUPPORTED_CONFIGURATION_FORMAT.value, title = "Unsupport", error_message = f"Unsupported configuration format: {lan or 'None'}").as_exception()

        if not output_str:
            raise DyError(ErrorDefs.FAILED.value, title = "Dump failed", error_message = f"Dump out format: {lan or 'None'}").as_exception()

        return output_str

    @staticmethod
    def load(file_path_like: Path|str, lan:TmlDefs|None = None, input_encoding:str|None = None, *args, **kwargs) -> dict[str,Any]:
        if not os.path.exists(file_path_like):
            raise DyError(ErrorDefs.NO_FILE_FOUND.value, title = "No file found", error_message = f"Lost file '{file_path_like}'").as_exception()

        file_path = Path(file_path_like) if isinstance(file_path_like, str) else file_path_like
        lan_en = TmlUtl.guess_file(file_path) if not lan else lan

        with file_path.open('rb') as fio:
            input_codec = codecs.lookup(input_encoding or 'utf-8')
            f = fio if input_codec.name == 'utf-8' else codecs.EncodedFile(fio, "utf-8", input_codec.name)

            match lan_en:
                case TmlDefs.JSON:
                    return json.load(f, *args, **kwargs)
                case TmlDefs.TOML:
                    return tomllib.load(f)
                case TmlDefs.YAML:
                    if yaml is None:
                        raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", error_message = "Can't import 'yaml' module").as_exception()
                    return yaml.load(f, Loader = yaml.Loader)
                case _:
                    raise DyError(ErrorDefs.UNSUPPORTED_CONFIGURATION_FORMAT.value, title = "Unsupport", error_message = f"Unsupported configuration format: {lan or 'None'}").as_exception()

    @staticmethod
    def load_attr(file_path_like: Path|str, lan: TmlDefs|None = None, input_encoding:str|None = None, *args, **kwargs) -> AttrDict | AttrList:
        rv = TmlUtl.load(file_path_like, lan, input_encoding, *args, **kwargs)
        return AttrList(rv) if isinstance(rv, list) else AttrDict(rv)

    @staticmethod
    def dump(obj: dict, file_path_like: Path|str, lan:TmlDefs|None = None, output_encoding:str|None = None, *args, **kwargs):
        if obj is None:
            raise DyError(ErrorDefs.ARGS_MUSTBE_EXIST.value, title = "No argument exist", error_message = "Miss 'obj' argument").as_exception()
        
        lan_en = TmlUtl.guess_file(file_path_like) if not lan else lan
        file_path = Path(file_path_like) if isinstance(file_path_like, str) else file_path_like
        

        # if not output_encoding: output_encoding = 'utf-8'
        # with file_path.open('rb') as fio:
        #     ef =  codecs.EncodedFile(fio, "utf-8", output_encoding)
        output_str: str|None = None

        match lan_en:
            case TmlDefs.JSON:
                output_str = json.dumps(obj, *args, **kwargs)
            case TmlDefs.TOML:
                raise DyError(ErrorDefs.UNSUPPORTED.value, title = "Unsuppoted", error_message = "Unsuppot dump").as_exception()
            case TmlDefs.YAML:
                if yaml is None:
                    raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", error_message = "Can't import 'yaml' module").as_exception()
                output_str = yaml.dump(obj, *args, **kwargs)
            case _:
                raise DyError(ErrorDefs.UNSUPPORTED_CONFIGURATION_FORMAT.value, title = "Unsupport", error_message = f"Unsupported configuration format: {lan or 'None'}").as_exception()

        if not output_str:
            raise DyError(ErrorDefs.FAILED.value, title = "Dump failed", error_message = f"Dump out format: {lan or 'None'}").as_exception()
        
        output_codec = codecs.lookup(output_encoding or 'utf-8')
        with file_path.open('wb') as fio:
            fio.write(output_str.encode(output_codec.name))