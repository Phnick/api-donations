from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id:Optional[int]=None
    name:str
    email:str
    password:str

    class Config:
        from_attributes = True

class User_simple(BaseModel):
    id:Optional[int]=None
    name:str
    email:str

    class Config:
        from_attributes = True

class Recover_password(BaseModel):
    email:str
    password:str

    class Config:
        from_attributes = True

class Login(BaseModel):
    email:str
    password:str

class Login_succes(BaseModel):
    user:User_simple
    token:str

