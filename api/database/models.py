from pydantic import BaseModel, ConfigDict
import datetime
import enum

class UserBase(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int

class CreateUser(UserBase):
    pass 

class Gender(enum.Enum):
    FEMALE="female"
    MALE = "male"

class PersonBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True, from_attributes=True)
    
    name: str
    age: int
    gender: Gender


class CreatePerson(PersonBase):
    pass

class Person(PersonBase):
    id: int
    updated_at: datetime.datetime
