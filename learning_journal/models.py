from sqlalchemy import (
    Column, Index, Integer, Text, Unicode, UnicodeText, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
import datetime


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False, unique=True)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def all(cls, session=None):
        """
        Returns all the entries in the database table, ordered so that the most
        recent entry is first.

        Parameters
        ==========
        session: session to use when running from interpreter
        """
        if session is None:
            session = DBSession
        results = session.query(cls).order_by(cls.edited.desc()).all()
        return results

    @classmethod
    def by_id(cls, id, session=None):
        """
        Returns a single entry, given an id.

        Parameters
        ==========
        id: id of the instance to return
        session: session to use when running from interpreter
        """
        id = int(id)  # convert to int
        if session is None:
            session = DBSession
        result = session.query(cls).get(id)
        return result
