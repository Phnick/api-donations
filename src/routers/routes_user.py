from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from schemas.schemas import User, User_simple, Recover_password, Login, Login_succes
from infra.sqlalchemy.config.database import get_db
from service.service_user import UserService
from routers.auth import get_user_logged


router = APIRouter()


@router.post('/sigup', status_code=status.HTTP_201_CREATED, response_model=User_simple)
def create_user(user: User, background_task: BackgroundTasks, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.user_create(user, background_task)


@router.put('/user', response_model=User_simple)
def edit_user_logged_in(user_update: User_simple, user_logged_in: User = Depends(get_user_logged), db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.edit_user(user_update, user_logged_in)


@router.post('/token', response_model=Login_succes)
def login(login: Login, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user, token = user_service.autentic_user(login.password, login.email)
    return Login_succes(user=user, token=token)


# verify if user stay logged in
@router.get('/me', response_model=User_simple)
def me(usuario_logado: User = Depends(get_user_logged)):
    return usuario_logado
