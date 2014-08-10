# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import *


class Model(object):
    def __init__(self):
        from sqlalchemy.engine.url import URL

        options = {'characterEncoding':'utf-8'}
        url = URL('mysql', username=DATABASE_USER, password=DATABASE_PASS, host=DATABASE_HOST, port=DATABASE_PORT,
                  database=DATABASE_DBNAME, query=options)
        engine = create_engine(url)
        dbsession = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

