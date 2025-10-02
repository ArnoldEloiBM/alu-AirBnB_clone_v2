#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    """City class that will be used to represent a city"""

    __tablename__ = "cities"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship(
            "Place", back_populates="cities", cascade="all, delete-orphan"
        )
        state = relationship("State", back_populates="cities")
    else:
        # for file storage
        state_id = ""  # it will be the state.id
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a City Instance"""
        super().__init__(*args, **kwargs)
