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
	body = Column(UnicodeText)
	created = Column(DateTime, default=datetime.datetime.now())
	edited = Column(DateTime, default=datetime.datetime.now())

	def all(self):
		"""
		Returns all the entries in the database table, ordered so that the most
		recent entry is first.
		"""
		results = DBSession.query(self).order_by(self.created.desc()).all()
		return results

	def by_id(self, id):
		"""
		Returns a single entry, given an id.
		"""
		result = DBSession.query(self).get(id)
		return result