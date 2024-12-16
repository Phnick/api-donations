from pydantic import BaseModel
from typing import Optional,List



class Donation_simple(BaseModel):
    id:Optional[int] = None
    item_name:str
    quantity:float
    description:str
    donor_id:Optional[int] =None
    
    class Config:
        from_attributes = True
   

class User(BaseModel):
    id:Optional[int]=None
    name:str
    email:str
    password:str
    donations_given:List[Donation_simple] = []

    
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

class Donation(BaseModel):
    id:Optional[int] = None
    item_name:str
    quantity:float
    description:str
    status:str = "Disponível"
    receiver_id :Optional[int] = None
    donor_id: Optional[int] = None
    donor:Optional[User_simple] = None

    class Config:
        from_attributes = True


class Donation_receiver(BaseModel):
     receiver_id :int
     receiver: Optional[User_simple] = None
     
     class Config:
        from_attributes = True


