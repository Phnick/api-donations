from sqlalchemy import create_engine
from infra.sqlalchemy.config.base import Base
from sqlalchemy.orm import sessionmaker
import mysql.connector
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
load_dotenv()


class BdConnectionHandler:
    def __init__(self):
        self.connection_string = f'mysql+mysqlconnector://{os.getenv("USUARIO")}:{os.getenv("SENHA")}@{os.getenv("SERVIDOR")}/{os.getenv("DATABASE")}'
        self.engine = self.create_database_engine()
        self.sessionlocal = self.create_session()
        

    def create_database_engine(self):
        engine = create_engine(self.connection_string, echo=True)
        return engine

    def create_session(self):
        SessionLocal = sessionmaker(bind=self.engine)
        return SessionLocal

    def get_engine(self):
        return self.engine

    def create_database_if_not_exist(self):
        try:
            # Conectando ao servidor MySQL sem especificar o banco de dados
            conn = mysql.connector.connect(
                user=os.getenv("USUARIO"),
                password=os.getenv("SENHA"),
                host=os.getenv("SERVIDOR")
            )
            cursor = conn.cursor()
            # Verifique se o banco de dados já existe
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {os.getenv('DATABASE')}")
            print(
                f"Banco de dados {os.getenv('DATABASE')} verificado/criado com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ou criar banco de dados: {err}")
        finally:
            cursor.close()
            conn.close()

    def create_bd(self):

        try:
            Base.metadata.create_all(bind=self.engine)
            print("Tabelas criadas com sucesso.")
        except SQLAlchemyError as e:
            print(f"Erro ao criar tabelas: {e}")

    # def get_db(self):
    #     db = self.sessionlocal
    #     try:
    #         yield db
    #     finally:
    #         db.close()

db_connection_handler = BdConnectionHandler()

# Função get_db usada como dependência
def get_db():
    db = db_connection_handler.sessionlocal()
    try:
        yield db
    finally:
        db.close()