from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from schemas.schemas import Donation,Donation_receiver,Donation_simple, User
from infra.sqlalchemy.config.database import get_db
from service.service_donations import DonationService
from routers.auth import get_user_logged

router = APIRouter()


@router.post('/donations',status_code=status.HTTP_201_CREATED,response_model=Donation)
def create_donation(donation:Donation,user_logged_in:User=Depends(get_user_logged),db:Session=Depends(get_db)):
    donation_service= DonationService(db)
    return donation_service.donation_create(donation,user_logged_in)