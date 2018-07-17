from sqlalchemy import (Column, String, Integer, ForeignKey)
from sqlalchemy.orm import relationship

from helpers.database import Base
from utilities.utility import Utility
from api.location.models import Location  # noqa: F401


class Office(Base, Utility):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location')
    blocks = relationship('Block')
