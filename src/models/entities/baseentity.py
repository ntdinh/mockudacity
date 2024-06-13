from __future__ import annotations

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

from src.helpers import CommonHelper


Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    Code = Column(String(12), primary_key=True)
    CreatedAt = Column(String(250))
    ModifiedAt = Column(String(250))

    def __init__(self, **params):
        self.Code = params['Code'] if 'Code' in params \
            else CommonHelper.instance().genUID()
        # Using below format to order by date string
        now = CommonHelper.instance() \
            .nowString(tz='Asia/Ho_Chi_Minh', fmt='%Y/%m/%d %H:%M:%S')
        self.CreatedAt = now
        self.ModifiedAt = now

    def copyFrom(self, entity: BaseEntity):
        if entity.ModifiedAt is not None:
            self.ModifiedAt = entity.ModifiedAt
