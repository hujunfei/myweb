# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from ubuntuone.syncdaemon.tritcask import timestamp
from sqlalchemy import create_engine, Column, Integer, String, Text, SmallInteger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import *


Base = declarative_base()


class Model(object):
    def __init__(self):
        from sqlalchemy.engine.url import URL

        #options = {'characterEncoding':'utf-8'}
        options = {}
        options['charset'] = "utf8"
        url = URL('mysql', username=DATABASE_USER, password=DATABASE_PASS, host=DATABASE_HOST, port=DATABASE_PORT,
                  database=DATABASE_DBNAME, query=options)
        engine = create_engine(url)
        self.conn = engine.connect()
        self.db_session = scoped_session(sessionmaker(bind=engine))

    def add_record(self, record):
        if not isinstance(record, Base):
            return False
        try:
            self.db_session.add(record)
            self.db_session.commit()
            return True
        except SQLAlchemyError, e:
            return False

    def update_record(self, record):
        if not issubclass(record, Base):
            return False

    def exe_sql(self, sql, *args, **kwargs):
        self.conn.execute(sql, *args, **kwargs)

Model = Model()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    category = Column(String(20), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(100), nullable=False)
    archive = Column(String(6), nullable=False)
    add_time = Column(Integer, nullable=False)
    edit_time = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        #Base.__init__(Article, super)
        if len(args) == 1:
            params = args[0]
            #if not isinstance(params, dict):
            #    return
            self.category = params['category']
            self.title = params['title']
            self.content = params['content']
            self.tags = params['tags'].replace(u'，',',')
            self.archive = genArchive()
            tm = int(timestamp())
            self.add_time = tm
            self.edit_time = tm
        else:
            params = kwargs
            self.category = params['category']
            self.title = params['title']
            self.content = params['content']
            self.tags = params['tags'].replace(u'，',',')
            self.archive = genArchive()
            tm = int(timestamp())
            self.add_time = tm
            self.edit_time = tm

    @staticmethod
    def add_article(params):
        if not isinstance(params, dict):
            return False
        article = Article(params)
        return Model.add_record(article)


def create_table():
    sql = """
CREATE TABLE IF NOT EXISTS `category` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL DEFAULT '',
  `id_num` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `content` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `archive` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(17) NOT NULL DEFAULT '',
  `id_num` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `content` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `comments` (
  `id` int(8) unsigned NOT NULL AUTO_INCREMENT,
  `postid` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `author` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `url` varchar(75) NOT NULL,
  `visible` tinyint(1) NOT NULL DEFAULT '1',
  `add_time` int(10) unsigned NOT NULL DEFAULT '0',
  `content` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `postid` (`postid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `links` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `displayorder` tinyint(3) NOT NULL DEFAULT '0',
  `name` varchar(100) NOT NULL DEFAULT '',
  `url` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `article` (
  `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(20) NOT NULL DEFAULT '',
  `title` varchar(100) NOT NULL DEFAULT '',
  `content` mediumtext NOT NULL,
  `tags` varchar(100) NOT NULL,
  `archive` varchar(6) NOT NULL DEFAULT '1',
  `add_time` int(10) unsigned NOT NULL DEFAULT '0',
  `edit_time` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `category` (`category`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `tags` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(17) NOT NULL DEFAULT '',
  `id_num` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `content` mediumtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `id_num` (`id_num`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `user` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL DEFAULT '',
  `password` varchar(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

"""
    Model.exe_sql(sql)

def cnnow():
    return datetime.utcnow() + timedelta(hours =+ 8)

#generate the archive name
def genArchive():
    #return "201207"
    return cnnow().strftime("%Y%m")

if __name__ == "__main__":
    params = {}
    params['category'] = "cat1"
    params['title'] = "Test测试文章"
    params['content'] = "测试内容"
    params['tags'] = 'python, web'
    Article.add_article(params)
    #create_table()