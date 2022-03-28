# -*- coding:utf-8 -*-
#!/usr/bin/env Python

from libdouya.core.deco import obj_d, svc_d
from libdouya.core.mgr import NamingMgr

@obj_d("a", "aa", alias_urls = ["x://a"])
class A:
    def __init__(self):
        pass

@svc_d("b", "bb", "bbb", alias_urls = ["x://b"])
class B:
    def __init__(self):
        pass

def test_object_naming():
    assert(isinstance(A(), A))
    assert(isinstance(NamingMgr.get_instance().new_naming(A), A))
    assert(isinstance(NamingMgr.get_instance().new_naming('a'), A))
    assert(isinstance(NamingMgr.get_instance().new_naming('aa'), A))
    assert(isinstance(NamingMgr.get_instance().new_naming('x://a'), A))
    assert(NamingMgr.get_instance().get_alias_urls(A) == ["x://a"])

def test_service_naming():
    b = B()
    assert(isinstance(b, B))

    b1 = NamingMgr.get_instance().new_naming(B)
    assert(isinstance(b1, B))
    assert(b != b1)

    b2 = NamingMgr.get_instance().new_naming('b')
    assert(isinstance(b2, B))
    assert(b1 == b2)

    b3 = NamingMgr.get_instance().new_naming('bb')
    assert(isinstance(b3, B))
    assert(b1 == b3)

    b4 = NamingMgr.get_instance().new_naming('x://b')
    assert(isinstance(b4, B))
    assert(b1 == b4)

    assert(NamingMgr.get_instance().get_alias_urls(B) == ["x://b"])