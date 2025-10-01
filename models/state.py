#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City", back_populates="state", cascade="all, delete-orphan"
        )
    else:
        # for file storage
        name = ""

    def __init__(self, *args, **kwargs):
        """initialize a state object"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def cities(self):
            from models import storage
            from models.city import City

            # list of cities of a particular state
            citys = []
            for obj in storage.all(City).values():
                if obj.state_id == self.id:
                    citys.append(obj)
            return citys
