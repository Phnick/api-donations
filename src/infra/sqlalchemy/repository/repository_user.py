from sqlalchemy.orm import Session
from schemas import schemas
from infra.sqlalchemy.models import models
from sqlalchemy import select, update, delete
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()


class RepositoryUser:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: schemas.User):
        db_user = models.Register_user(name=user.name,
                                       email=user.email,
                                       password=user.password
                                       )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_email(self, email: str):
        query = select(models.Register_user).where(
            models.Register_user.email == email)
        user = self.db.execute(query).scalar()
        return user

    def edit_user(self, user_update: schemas.User_simple):
        user = update(models.Register_user).where(models.Register_user.id == user_update.id).values(name=user_update.name,
                                                                                                    email=user_update.email
                                                                                                    )
        self.db.execute(user)
        self.db.commit()

    def get_id(self, user_id: int):
        search = select(models.Register_user).where(
            models.Register_user.id == user_id)
        user = self.db.execute(search).scalar()
        return user

    def delete_user(self, user_id: int):
        delete_stmt = delete(models.Register_user).where(
            models.Register_user.id == user_id)
        self.db.execute(delete_stmt)
        self.db.commit()

    def list_user(self, user_id: int):
        user = self.db.query(models.Register_user).where(
            models.Register_user.id == user_id)
        return user

    def recover_password(self, user_update: schemas.Recover_password):
        new_password = update(models.Register_user).where(
            models.Register_user.email == user_update.email).values(password=user_update.password)
        self.db.execute(new_password)
        self.db.commit()

    def send_email(self, to_email: str, subject: str, body: str):

        from_email = os.getenv('FOM_EMAIL')
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = os.getenv('FROM_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        except Exception as e:
            # Log the exception or handle the error as necessary
            print(f"Erro ao enviar email: {e}")
