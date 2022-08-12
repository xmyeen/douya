# -*- coding:utf-8 -*-
#!/usr/bin/env python

from __future__ import absolute_import, print_function

from pony.orm import PrimaryKey,Required,Set
from sqlalchemy import Column, ForeignKey, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from libdouya.definations.db import OrmDef
from libdouya.definations.cfg import ConfigerDefs
from libdouya.dataclasses.c.db import Databases
from libdouya.core.rdb.orm import mkdb
from libdouya.core.mgr import ConfigurationMgr
import libdouya.core.configer.db.database_configer
import libdouya.core.rdb.orm.pony_database
import libdouya.core.rdb.orm.sql_alchemy_database
# from decimal import Decimal, Subnormal

def test_sqlalchemy_dml():
    db = mkdb(OrmDef.SQLALCHEMY_ORM.value)
    class Course(db.entity):
        __tablename__ = 'sa_course_tbl'
        id = Column(Integer, primary_key = True, autoincrement = True)
        name = Column(String(64), nullable = False)
    #     students = Set("Student")

    class Student(db.entity):
        __tablename__ = "sa_student_tbl"
        id = Column(Integer, primary_key = True, autoincrement = True)
        name = Column(String(64), nullable = False)
        course_id = Column(Integer, ForeignKey("sa_course_tbl.id", ondelete='CASCADE'), nullable = False)
        course = relationship('Course', backref='students')

    # class Student(db.entity):
    #     id = PrimaryKey(int, auto = True)
    #     name = Required(str)
    #     course = Required(Course)
    db.init()
    with db.on_session() as session:
        c1 = Course(name = "语文")
        session.add(c1)
        session.commit()
        session.flush()

        s1 = Student(name = "李磊", course_id = c1.id)
        s2 = Student(name = "韩梅梅", course_id = c1.id)
        session.add_all([s1, s2])
        session.commit()
        
        datas = session.query(Student).all()
        assert(2 == len(datas))

def test_pony_simple():
    db = mkdb(OrmDef.PONY_ORM.value)

    class Course(db.entity):
        id = PrimaryKey(int, auto = True)
        name = Required(str)
        students = Set("Student")

    class Student(db.entity):
        id = PrimaryKey(int, auto = True)
        name = Required(str)
        course = Required(Course)

    db.init()
    with db.on_session() as session:
        c1 = Course(name = "语文")
        s1 = Student(name = "李磊", course = c1)
        s2 = Student(name = "韩梅梅", course = c1)
        db.commit(session)

        datas = [ o for o in Student.select() if o in [s1, s2] ]
        assert(2 == len(datas))

def test_pony_configuration(make_db_from_configuration):
    db = make_db_from_configuration

    class Course(db.entity):
        id = PrimaryKey(int, auto = True)
        name = Required(str)
        students = Set("Student")

    class Student(db.entity):
        id = PrimaryKey(int, auto = True)
        name = Required(str)
        course = Required(Course)

    dbs = Databases(db)

    with ConfigurationMgr.get_instance().get_configer(ConfigerDefs.DB.value) as cf:
        cf.init_db(dbs)

    with dbs.db().on_session() as s:
        c1 = Course(name = "语文")
        s1 = Student(name = "李磊", course = c1)
        s2 = Student(name = "韩梅梅", course = c1)
        dbs.db().commit(s)

        datas = [ o for o in Student.select() if o in [s1, s2] ]
        assert(2 == len(datas))

# db.core.bind(provider='postgres', user='testor', password='testor', host='10.19.156.28', port=30432, database='testdb')
# sql_debug(True)
# db.core.generate_mapping(create_tables = True)
# db.init(db_url = 'postgresql://testor:testor@10.19.156.28:30432/testdb')