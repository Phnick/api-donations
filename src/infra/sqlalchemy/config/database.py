from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
load_dotenv()



SGBD = os.getenv('SGBD')
usuario = os.getenv('USUARIO')
senha = os.getenv('SENHA')
servidor = os.getenv('SERVIDOR')
database = os.getenv('DATABASE')
SQLALCHEMY_DATABASE_URL =\
    f'{SGBD}://{usuario}:{senha}@{servidor}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# criu o banco de dados


def criar_bd_se_não_existe():
    conn = mysql.connector.connect(user=usuario, password=senha, host=servidor)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conn.commit()
    cursor.close()
    conn.close()


def criar_bd():
    criar_bd_se_não_existe()
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

