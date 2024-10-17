from sqlalchemy.orm import Session
from schemas import schemas
from infra.sqlalchemy.models import models
from sqlalchemy import select,update,delete



class RepositoryDonation:
    def __init__(self,db:Session):
        self.db = db


    def create(self,donation:schemas.Donation):
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
    

    def edit_donations(self):
        pass

        