from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends,BackgroundTasks,status
# from infra.sqlalchemy.models.models import Usuario
from infra.sqlalchemy.repository.repository_user import RepositoryUser
from infra.providers import hash,token
from schemas.schemas import User,User_simple,Recover_password


class UserService:
    def __init__(self,db:Session):
        self.db = db
        self.repository_user = RepositoryUser(db)

    def user_create(self,user:User):
        if not user.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='error,campo name nao preenchido')    
        if not user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='error,campo email nao preenchido')
        if not user.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='error,campo password nao preenchido')
        
        localized_user = self.repository_user.get_email(user.email)  
        if localized_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='email ja cadastrado') 

        user.password = hash.create_hash(user.password) 
        user_created = self.repository_user.create(user)   
        return user_created 