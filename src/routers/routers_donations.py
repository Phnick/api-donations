from fastapi import APIRouter,Depends,status,BackgroundTasks
from sqlalchemy.orm import Session
from schemas.schemas import Donation,Donation_receiver,Donation_simple, User
from infra.sqlalchemy.config.database import get_db
from service.service_donations import DonationService
from routers.auth import get_user_logged

router = APIRouter()


@router.post('/donations',status_code=status.HTTP_201_CREATED,response_model=Donation)
def rota_criar_donation(donation:Donation,user_logged_in:User=Depends(get_user_logged),db:Session=Depends(get_db)):
    donation_service= DonationService(db)
    return donation_service.service_create(donation,user_logged_in)

@router.put('/donations/{donation_id}',response_model=Donation_receiver)
def rota_editar_receiver_id(donation_id:int,background_task:BackgroundTasks,usuario_logado:User=Depends(get_user_logged),db:Session=Depends(get_db)):
    donation_service = DonationService(db)
    update = donation_service.service_receive(donation_id,usuario_logado,background_task)
    return update

@router.get('/donations/{donation_id}',status_code=status.HTTP_200_OK,response_model=Donation)
def rota_buscar_donations(donation_id:int, db:Session=Depends(get_db)):
    donation_service  =DonationService(db)
    return donation_service.service_search_donations(donation_id)

@router.get('/donations/{donor_id}/user',response_model=list[Donation])
def rota_buscar_donation_donorid(donor_id:int,usuario_logado:User=Depends(get_user_logged),db:Session=Depends(get_db)):
    donation_service = DonationService(db)
    return donation_service.service_get_donations_by_donor(donor_id,usuario_logado)


@router.get('/donations',status_code=status.HTTP_200_OK,response_model=list[Donation])
def rota_listar_donation(db:Session=Depends(get_db)):
    donations_service = DonationService(db)
    return donations_service.service_list_donation()

@router.put('/donations/{id}/edit',status_code=status.HTTP_200_OK,response_model=Donation_simple)
def rota_editar_donation(id:int,donation:Donation_simple,usuario_logado:User=Depends(get_user_logged),db:Session=Depends(get_db)):
    donation_service =DonationService(db)
    atualizar = donation_service.service_edit_donation(id,donation,usuario_logado)
    return atualizar

@router.delete('/donations/{donation_id}')
def rota_delete_donation(donation_id:int,usuario_logado:User=Depends(get_user_logged),db:Session=Depends(get_db)):
    donation_service =DonationService(db)
    donation_service.service_delete(donation_id,usuario_logado)
    return f'A doação com o id: {donation_id}, foi deletado com sucesso!'