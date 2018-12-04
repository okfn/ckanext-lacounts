# encoding: utf-8

import uuid
import logging

from sqlalchemy import Column, Unicode, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

from ckan.model.meta import metadata

log = logging.getLogger(__name__)


def make_uuid():
    return unicode(uuid.uuid4())


Base = declarative_base(metadata=metadata)


class Event(Base):
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
