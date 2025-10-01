#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Review(BaseModel, Base):
    """Review class to store review information"""

    __tablename__ = "reviews"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        user = relationship("User", back_populates="reviews")
        place = relationship("Place", back_populates="reviews")
    else:
        # for file storage
        place_id = ""  # it will be the Place.id
        user_id = ""  # it will be the User.id
        text = ""

    def __init__(self, *args, **kwargs):
        """instantiate a review object"""
        super().__init__(*args, **kwargs)
