# encoding: utf-8

import uuid
import logging
import datetime

from sqlalchemy import Column, Unicode, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import orm
from sqlalchemy.util import OrderedDict

from ckan.model.meta import metadata, Session

log = logging.getLogger(__name__)


def make_uuid():
    return unicode(uuid.uuid4())


Base = declarative_base(metadata=metadata)


class LACountsBaseModel(object):

    @classmethod
    def filter(cls, **kwargs):
        return Session.query(cls).filter_by(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        instance = cls.filter(**kwargs).first()
        return instance

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        Session.add(instance)
        Session.commit()
        return instance.as_dict()

    @classmethod
    def count(cls):
        return Session.query(cls).count()

    @classmethod
    def list(cls, **kwargs):
        query = Session.query(cls)

        limit = kwargs.get('limit')
        if limit:
            query = query.limit(limit)

        offset = kwargs.get('offset')
        if offset:
            query = query.offset(offset)

        event_dicts = [event.as_dict() for event in query.all()]

        return event_dicts

    def save(self):
        Session.add(self)
        Session.commit()
        return self.as_dict()

    def as_dict(self):
        _dict = OrderedDict()
        table = orm.class_mapper(self.__class__).mapped_table
        for col in table.c:
            val = getattr(self, col.name)
            if isinstance(val, datetime.date):
                val = str(val)
            if isinstance(val, datetime.datetime):
                val = val.isoformat()
            _dict[col.name] = val
        return _dict

    def delete(self):
        Session.delete(self)
        Session.commit()


class Event(LACountsBaseModel, Base):
    __tablename__ = u'events'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    name = Column(Unicode)
    url = Column(Unicode)
    date = Column(DateTime)
    free = Column(Boolean)
    topic_tags = Column(JSON)


def create_tables():
    Event.__table__.create()

    log.info(u'Event database tables created')


def tables_exist():
    return Event.__table__.exists()
