from fastapi import APIRouter,Depends,status,BackgroundTasks
from sqlalchemy.orm import Session
from schemas.schemas import User,User_simple,Recover_password,Login,Login_succes
from infra.sqlalchemy.config.database import get_db
from service.service_user import UserService


router = APIRouter()

@router.post('/sigup',status_code=status.HTTP_201_CREATED, response_model=User_simple)
def create_user(usuario:User,db:Session=Depends(get_db)):
    user_service =UserService(db)
    return user_service.user_create(usuario)
