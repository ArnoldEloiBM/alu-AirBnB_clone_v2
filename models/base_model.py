#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from datetime import datetime
import models


# sqlalchemy

Base = declarative_base()


class BaseModel:
    """
    BaseModel class that defines common methods and attributes for other
    classes.

    This class provides methods for managing unique object identifiers,
    timestamps for creation and updates, and converting instances into
    dictionary representations.

    Attributes:
        id (str): Unique identifier for each instance, generated using UUID.
        created_at (datetime): Timestamp when the instance was created.
        updated_at (datetime): Timestamp when the instance was last updated.

    Methods:
        __str__(): Returns a string representation of the instance.
        save(): Updates the 'updated_at' timestamp and saves the instance.
        to_dict(): Converts the instance to a dictionary including all
                   instance attributes.
    """

    # class attributes
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    # public instances
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        Args:
            *args: Variable length argument list (not used in this class).
            **kwargs: Dictionary of keyword arguments to populate instance
                      attributes.
                - If no kwargs, a new UUID and timestamp are generated.
                - If kwargs are provided, the instance is populated with the
                  given values.

        Example:
            base_instance = BaseModel(id="123",
            created_at="2025-01-01T00:00:00",
            updated_at="2025-01-01T01:00:00")
        """
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "updated_at":
                        setattr(self, key, datetime.fromisoformat(value))
                    elif key == "created_at":
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)  # some updates..

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: A formatted string with the class name, instance ID, and a
                 dictionary of its attributes.

        Example:
            "[BaseModel] (1234) {'id': '1234',
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T01:00:00'}"
        """
        # return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    # public methods
    def save(self):
        """
        Updates the 'updated_at' attribute with the current datetime and saves
        the instance.

        This method updates the instance's 'updated_at' field and adds the
        instance to the storage. Calls the 'new' and 'save' methods from the
        storage module to persist the changes.

        Example:
            base_instance.save()
        """
        self.updated_at = datetime.today()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the instance with all
        attributes.

        The dictionary includes the 'created_at' and 'updated_at' attributes as
        ISO format strings and also adds the '__class__' key to indicate the
        class type.

        Returns:
            dict: A dictionary of instance attributes including class name and
                  timestamps.

        Example:
            {
                'id': '1234',
                'created_at': '2025-01-01T00:00:00',
                'updated_at': '2025-01-01T01:00:00',
                '__class__': 'BaseModel'
            }
        """
        instance_dict = self.__dict__.copy()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["__class__"] = self.__class__.__name__

        # updates to remove _sa_instance_state if exists from
        if "_sa_instance_state" in instance_dict.keys():
            del instance_dict["_sa_instance_state"]
        return instance_dict

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)
