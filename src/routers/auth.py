from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from infra.sqlalchemy.config.database import get_db
from infra.providers import token_providers
from jose import JWTError
from infra.sqlalchemy.repository.repository_user import RepositoryUser

oauth_schemas = OAuth2PasswordBearer(tokenUrl = 'token')

def get_user_logged(token:str = Depends(oauth_schemas),db:Session=Depends(get_db)):
    try:
        email = token_providers.check_access_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Token invalido')     
    

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='email nao encontrado')
    
    user = RepositoryUser(db).get_email(email)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='usuario não encontrado')
    
    return user