from datetime import datetime,timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
EXPIRES_IN_MINUTES = 60

# cria um token jwt com expiração
def cerate_access_token(data:dict):
    dados = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MINUTES)


    dados.update({'exp': expires})
    token_jwt = jwt.encode(dados,SECRET_KEY,algorithm = ALGORITHM)
    return token_jwt



def check_access_token(token:str):
    carga = jwt.decode(token, SECRET_KEY,algorithms = [ALGORITHM])
    return carga.get('sub')