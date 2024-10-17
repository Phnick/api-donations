from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends
from infra.sqlalchemy.repository.repository_donations import RepositoryDonation
from schemas.schemas import Donation,Donation_receiver,Donation_simple
from schemas.schemas import User


class DonationService:
    def __init__(self,db:Session):
        self.db = db
        self.repository_donation = RepositoryDonation(db)

    # Create donation
    def donation_create(self,donation:Donation,user_logged_inf:User):
        if not donation.item_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='erro,campo obrigatório')
        
        if not donation.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='erro,campo obrigatório')
        
        if not donation.description:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='erro,campo obrigatório')
        
        if not donation.status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='erro,campo obrigatório')
        
        if not donation.donor_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='erro,campo obrigatório')
        
        
        
        if not user_logged_inf:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='usuario não logado')

        donation.id = user_logged_inf.id
        donation_create =self.repository_donation.create(donation)
        return donation_create