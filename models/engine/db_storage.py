import models
from models.base_model import Base
from models.city import City
from models.pitch import Pitch
from models.pitch_owner import PitchOwner
from models.reservation import Reservation
from models.review import Review
from models.user import User
import json


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import urllib

classes = {"City": City, "Pitch": Pitch, "PitchOwner": PitchOwner, "Reservation": Reservation, "Review": Review, "User": User}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        with open('local.settings.json') as f:
            settings = json.load(f)
        # Get the connection string
        conn_str = settings.get('Values').get('ODBCConnectionString')
        params = urllib.parse.quote_plus(conn_str)
        self.__engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count