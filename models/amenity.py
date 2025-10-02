#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv


class Amenity(BaseModel, Base):
    """info to be filled"""

    __tablename__ = "amenities"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        from models.place import Place

        place_amenities = relationship(
            "Place", secondary=Place.place_amenity, back_populates="amenities"
        )
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
