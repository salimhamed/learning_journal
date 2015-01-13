from sqlalchemy import (
    Column, Index, Integer, Text, Unicode, UnicodeText, DateTime
)
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255))
    body = Column(UnicodeText)
    created = Column(DateTime)
    edited = Column(DateTime)
