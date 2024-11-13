from sqlalchemy.orm import Session
from schemas import schemas
from infra.sqlalchemy.models import models
from sqlalchemy import select,update,delete
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()



class RepositoryDonation:
    def __init__(self,db:Session):
        self.db = db


    def create_donation(self,donation:schemas.Donation):
        db_donation = models.Donations(item_name = donation.item_name,
                                       quantity=donation.quantity,
                                       description=donation.description,
                                       status=donation.status,
                                       donor_id=donation.donor_id,
                                       receiver_id=donation.receiver_id)
        self.db.add(db_donation)
        self.db.commit()
        self.db.refresh(db_donation)
        return db_donation
    
    # fazer o editar a doação onde o donor_id, nao vai ser atualizado apenas as informçoes
    def update_donation(self,id:int,donation:schemas.Donation_simple):
        update_stmt = update(models.Donations).where(models.Donations.id == id).values(item_name = donation.item_name,
                                                                                       quantity = donation.quantity,
                                                                                       description = donation.description)
        self.db.execute(update_stmt)
        self.db.commit()
    
    # aqui eu vou pegar o id da doação e se bater com o id que eu tenho no BD eu vou alterar a penas o receiver_id,que no service vai ser igual ao id do usuario logado
    def update_receive(self,donation_id:int,receiver_id:int):
        update_receive = update(models.Donations).where(models.Donations.id == donation_id).values(receiver_id=receiver_id)
        self.db.execute(update_receive)
        self.db.commit()
    
    # aqui eu pego id do doador para fazer verificações
    def select_donor_id(self,donor_id:int):
        search = select(models.Donations).where(models.Donations.donor_id == donor_id)
        donor = self.db.execute(search).scalar()
        return donor  
    
    # buscar uma doação atraves do id 
    def select_id_donation(self,id:int):
        buscar_stmt = select(models.Donations).where(models.Donations.id == id)
        donation = self.db.execute(buscar_stmt).scalars().one_or_none()
        return donation
    
    #  a lista de doaçoes
    def list_donations(self):
        donations  = self.db.query(models.Donations).all()
        return donations
    
    # pega as doaçoes de um doador especifico
    def get_donations_by_donor(self, donor_id:int):
        donations = self.db.query(models.Donations).where(models.Donations.donor_id == donor_id).all()
        return donations
    
    
    # vamos enviar um email para o doador que a pessoa teve interresse na doação
    def send_email(self,to_email:str,subject:str,body:str):

        from_email = os.getenv('FOM_EMAIL')
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = os.getenv('FROM_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')

        msg=EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        try:
            with smtplib.SMTP(smtp_server,smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        except Exception as e:
            # Log the exception or handle the error as necessary
            print(f"Erro ao enviar email: {e}")  
                  
    # deletar uma doação pelo id
    def delete_donation(self,donation_id:int):
        delete_stmt = delete(models.Donations).where(models.Donations.id  == donation_id)
        self.db.execute(delete_stmt)
        self.db.commit()
         
    