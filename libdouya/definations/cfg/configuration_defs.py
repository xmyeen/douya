# -*- coding:utf-8 -*-
#!/usr/bin/env python

from attrbox import AttrDict
import enum

DY_CONFIGURATION_KEY_DEF = AttrDict(
    # 错误码配置项
    ERROR = "err",
    ERROR_URL = "err.url",
    # 数据库配置项
    DATABASE = "db",
    PRIMARY_DATABASE = "db.priv",
    PRIMARY_DATABASE_URL = "db.priv.url",
    # 服务配置项
    SERVICE = "srv",
    HTTP_SERVICE = "srv.httpd",
    HTTP_SERVICE_HOST = "srv.httpd.host",
    HTTP_SERVICE_PORT = "srv.httpd.port",
    # 目录配置项
    CATALOG = "catalog",
    BINARY_CATALOG_DIR = "catalog.bin_dir",
    DATA_CATALOG_DIR = "catalog.data_dir",
    TEMPORARY_CATALOG_DIR = "catalog.temp_dir",
    BACKUP_CATALOG_DIR = "catalog.backup_dir",
    # 日志配置项
    LOGGER = "log"
)

@enum.unique
class ConfigerDefs(enum.Enum):
    ERR = "DY:ERROR"
    DB = "DY:DATABASE"
    # SVR = "DY:SERVER"
    SRV = "DY:SERVICE"
    DATACACHE = "DY:DATACACHE"