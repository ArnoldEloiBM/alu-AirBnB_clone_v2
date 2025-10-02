#!/usr/bin/python3
"""Database model"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

# from dotenv import load_dotenv, find_dotenv
# env_path = find_dotenv(".env")
# load_dotenv(env_path)


class DBStorage:
    """to be edited"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_DB = os.getenv("HBNB_MYSQL_DB")
        HBNB_MYSQL_HOST = os.getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_USER = os.getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = os.getenv("HBNB_MYSQL_PWD")
        HBNB_ENV = os.getenv("HBNB_ENV")

        # db = (
        #     f"mysql+mysqldb://{HBNB_MYSQL_USER}:"
        #     f"{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/"
        #     f"{HBNB_MYSQL_DB}"
        # )
        db = "mysql+mysqldb://{}:{}@{}/{}".format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB
        )
        self.__engine = create_engine(db, pool_pre_ping=True)

        # drop all tables if HBNB_ENV == test
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        if cls is not None:
            objs_dict = {
                # f"{obj.__class__.__name__}.{obj.id}": obj
                "{}.{}".format(obj.__class__.__name__, obj.id): obj
                for obj in self.__session.query(cls)
            }
            return objs_dict
        else:
            classes = [
                State,
                Review,
                User,
                Place,
                City,
            ]
            objs_dict = {}
            for item in classes:
                for obj in self.__session.query(item):
                    # objs_dict[f"{obj.__class__.__name__}.{obj.id}"] = obj
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objs_dict[key] = obj
            return objs_dict

    def new(self, obj):
        """add the object to the current database session"""
        if self.__session is not None:
            self.__session.add(obj)
        else:
            # for test purposes
            print("session not started.")

    def save(self):
        """commit all changes of the current database session"""
        if self.__session is not None:
            self.__session.commit()
        else:
            # for test purposes
            print("session not started.")

    def delete(self, obj=None):
        """delete obj (if not None) from the current database session"""
        if obj is not None:
            self.__session.delete(obj)  # mark the object for deletion
            # self.__session.commit()  # save the changes (delete the object)
        else:
            print("No object provided for deletion")

    def reload(self):
        """create all tables in the database"""

        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """class close"""
        self.__session.close()
