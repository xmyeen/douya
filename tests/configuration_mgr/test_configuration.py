# -*- coding:utf-8 -*-
#!/usr/bin/env python

import os, json, tempfile
from libdouya.definations.cfg.env_defs import EnvDefs, EnvFilterModeDef, EnvSelectModeDef
from libdouya.core.mgr import ConfigurationMgr

def test_base_function():
    ConfigurationMgr.get_instance().init()

    assert(isinstance(ConfigurationMgr.get_instance().configuration, dict))
    assert(isinstance(ConfigurationMgr.get_instance().get_conf("srv.httpd"), dict))
    assert(isinstance(ConfigurationMgr.get_instance().get_conf("db"), dict))
    assert(isinstance(ConfigurationMgr.get_instance().get_conf("log"), dict))
    assert(isinstance(ConfigurationMgr.get_instance().get_conf("catalog.bin_dir"), str))
    assert(isinstance(ConfigurationMgr.get_instance().get_conf("catalog.temp_dir"), str))
    assert(isinstance(ConfigurationMgr.get_instance().get_conf("catalog.backup_dir"), str))
    assert(isinstance(ConfigurationMgr.get_instance().get_conf("catalog.data_dir"), str))

def test_catalog():
    ConfigurationMgr.get_instance().init()
    assert(os.path.abspath("var") == ConfigurationMgr.get_instance().as_data_diretory())
    assert(os.path.abspath("var/1") == ConfigurationMgr.get_instance().as_data_diretory("1"))
    assert(os.path.abspath("var/1/2") == ConfigurationMgr.get_instance().as_data_diretory("1/2"))

    assert(os.path.abspath("bin") == ConfigurationMgr.get_instance().as_binary_diretory())
    assert(os.path.abspath("bin/1") == ConfigurationMgr.get_instance().as_binary_diretory("1"))
    assert(os.path.abspath("bin/1/2") == ConfigurationMgr.get_instance().as_binary_diretory("1/2"))

    assert(os.path.abspath("tmp") == ConfigurationMgr.get_instance().as_temporary_diretory())
    assert(os.path.abspath("tmp/1") == ConfigurationMgr.get_instance().as_temporary_diretory("1"))
    assert(os.path.abspath("tmp/1/2") == ConfigurationMgr.get_instance().as_temporary_diretory("1/2"))

    assert(os.path.abspath("bak") == ConfigurationMgr.get_instance().as_backup_diretory())
    assert(os.path.abspath("bak/1") == ConfigurationMgr.get_instance().as_backup_diretory("1"))
    assert(os.path.abspath("bak/1/2") == ConfigurationMgr.get_instance().as_backup_diretory("1/2"))


def test_merge_configuration():
    ConfigurationMgr.get_instance().init()

    assert(os.path.abspath("var") == ConfigurationMgr.get_instance().as_data_diretory())

    with tempfile.TemporaryDirectory() as td:
        name = os.path.join(td, 'test_merge_configuration.json')
        with open(name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(dict(catalog = dict(data_dir = "abc")), ensure_ascii=False))
            f.flush()

        ConfigurationMgr.get_instance().load_configuration_file(name)
        assert(os.path.abspath("abc") == ConfigurationMgr.get_instance().as_data_diretory())

def test_appenv_confs(make_temp_env_of_app_cfg):
    app_env = "dev"
    app_cfg_dir = os.environ.get(EnvDefs.APP_CFG_DIR.name)
    app_cfg_name = os.environ.get(EnvDefs.APP_CFG_NAME.name)
    data_dir_info = dict(non = "data_dir_on_default", devel = "data_dir_in_devel")

    with open(os.path.join(app_cfg_dir, app_cfg_name), 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict(catalog = dict(data_dir = data_dir_info["non"])), ensure_ascii=False))
        f.flush()

    with open(os.path.join(app_cfg_dir, f"-{app_env}".join(os.path.splitext(app_cfg_name))), 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict(catalog = dict(data_dir = data_dir_info["devel"])), ensure_ascii=False))
        f.flush()

    ConfigurationMgr.get_instance().init(None)
    assert(os.path.abspath(data_dir_info["non"]) == ConfigurationMgr.get_instance().as_data_diretory())

    ConfigurationMgr.get_instance().init(app_env)
    assert(os.path.abspath(data_dir_info["devel"]) == ConfigurationMgr.get_instance().as_data_diretory())

def test_appenv_files(make_temp_env_of_lookup):
    app_env = "dev"
    filename = "test_lookup.csv"
    lookup_dirs = os.environ.get(EnvDefs.APP_LOOKUP_DIR.name).split(":")
    for lookup_dir in lookup_dirs:
        with open(os.path.join(lookup_dir, filename), 'w', encoding='utf-8') as f:
            f.write("name\nZhangsan")
            f.flush()

        with open(os.path.join(lookup_dir, f"-{app_env}".join(os.path.splitext(filename))), 'w', encoding='utf-8') as f:
            f.write("name\nLisi")
            f.flush()

        lookup_subdir = os.path.join(lookup_dir, 'sub')
        if not os.path.exists(lookup_subdir):
            os.makedirs(lookup_subdir)
        with open(os.path.join(lookup_subdir, f"-{app_env}".join(os.path.splitext(filename))), 'w', encoding='utf-8') as f:
            f.write("name\nLisi")
            f.flush()


    ConfigurationMgr.get_instance().init(app_env)

    for en in EnvFilterModeDef.__members__.values():
        cfg = dict(filter_mode = en.name, select_mode = EnvSelectModeDef.ANY.name, walking_subdirs = False, containing_env_dirs = False)
        assert(1 == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))
        cfg = dict(filter_mode = en.name, select_mode = EnvSelectModeDef.ANY.name, walking_subdirs = True, containing_env_dirs = False)
        assert(1 == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))

    cfg = dict(filter_mode = EnvFilterModeDef.ALL.name, select_mode = EnvSelectModeDef.ALL.name, walking_subdirs = False, containing_env_dirs = False)
    assert((len(lookup_dirs) * 2) == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))
    cfg = dict(filter_mode = EnvFilterModeDef.ALL.name, select_mode = EnvSelectModeDef.ALL.name, walking_subdirs = True, containing_env_dirs = False)
    assert((len(lookup_dirs) * 3) == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))

    cfg = dict(filter_mode = EnvFilterModeDef.ENV_FILES_FIRST.name, select_mode = EnvSelectModeDef.ALL.name, walking_subdirs = False, containing_env_dirs = False)
    assert((len(lookup_dirs) * 1) == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))
    cfg = dict(filter_mode = EnvFilterModeDef.ENV_FILES_FIRST.name, select_mode = EnvSelectModeDef.ALL.name, walking_subdirs = True, containing_env_dirs = False)
    assert((len(lookup_dirs) * 2) == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))

    cfg = dict(filter_mode = EnvFilterModeDef.ONLY_ENV_FILES.name, select_mode = EnvSelectModeDef.ALL.name, walking_subdirs = False, containing_env_dirs = False)
    assert((len(lookup_dirs) * 1) == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))
    cfg = dict(filter_mode = EnvFilterModeDef.ONLY_ENV_FILES.name, select_mode = EnvSelectModeDef.ALL.name, walking_subdirs = True, containing_env_dirs = False)
    assert((len(lookup_dirs) * 2) == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))

    cfg = dict(filter_mode = EnvFilterModeDef.EXINCLUDING_ENV_FILES.name, select_mode = EnvSelectModeDef.ALL.name, walking_subdirs = False, containing_env_dirs = False)
    assert((len(lookup_dirs) * 1) == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))
    cfg = dict(filter_mode = EnvFilterModeDef.EXINCLUDING_ENV_FILES.name, select_mode = EnvSelectModeDef.ALL.name, walking_subdirs = True, containing_env_dirs = False)
    assert((len(lookup_dirs) * 1) == len(list(ConfigurationMgr.get_instance().walk_appenv_files(filename, **cfg))))