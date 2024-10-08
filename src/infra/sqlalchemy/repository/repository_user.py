from sqlalchemy.orm import Session
from schemas import schemas
from infra.sqlalchemy.models import models
from sqlalchemy import select,update,delete
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

class RepositoryUser:
    def __init__(self,db:Session):
        self.db = db

    def create(self,user:schemas.User):
        db_user = models.Register_user(name=user.name,
                                       email=user.email,
                                       password=user.password
                                       )     
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_email(self,email:str):
        query = select(models.Register_user).where(models.Register_user.email == email)
        user = self.db.execute(query).scalar()
        return user
