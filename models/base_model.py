"""
Class that will serve as a base model for all the models in the database
"""


from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import uuid4


time = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel(SQLModel):
    """The model class from which the others classes will be derived"""

    id: str = Field(default_factory=lambda: str(uuid4()), max_length=128, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    
    
    def __str__(self) -> str:
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
        
    def to_dict(self) -> dict:
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        if "start_time" in new_dict:
            new_dict["start_time"] = new_dict["start_time"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict