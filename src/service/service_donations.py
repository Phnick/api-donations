from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends,BackgroundTasks
from infra.sqlalchemy.repository.repository_donations import RepositoryDonation
from infra.sqlalchemy.repository.repository_user import RepositoryUser
from schemas.schemas import Donation,Donation_receiver,Donation_simple
from schemas.schemas import User,User_simple


class DonationService:
    def __init__(self,db:Session):
        self.db = db
        self.repository_donation = RepositoryDonation(db)
        self.repository_user = RepositoryUser(db)

    # regra de negócio para criar uma doação
    def service_create(self,donation:Donation,user_logged_in:User):
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
        
        if not user_logged_in:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='usuario não logado')
        # dar uma olhada melhor para que nao precise colocar o id de quem ta doando so de estar logado ja pegar o id
        donation.donor_id  = user_logged_in.id

        donation.id = user_logged_in.id
        donation_create =self.repository_donation.create_donation(donation)
        return donation_create
    
    # regra de negócios para pegar a doação e com isso atualizar o receive_id da doação
    def service_receive(self,donation_id:int,usuario_logado:User,background_task:BackgroundTasks):
        donation = self.repository_donation.select_id_donation(donation_id)
        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Doaçãonão encontrada')
        donation.receiver_id = usuario_logado.id
        
        donor_id = donation.donor_id
        donation_id = donation.receiver_id
        
        donor = self.repository_donation.select_donor_id(donor_id)
        if not donor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='doador nao encontrado')
        donation.status ='indisponivel'
        
        receiver_info = self.repository_user.get_id(donation_id)
        donor_info = self.repository_user.get_id(donor_id)
        
        subject = 'Sua doação foi selecionada'
        body = f'Olá {donor_info.name} tudo bem?\n\n O {receiver_info.name} com email: {receiver_info.email} tem interesse na sua doação!' 
        background_task.add_task(self.repository_donation.send_email,donor_info.email,subject,body)
        
        self.repository_donation.update_receive(donation_id,donation.receiver_id)
        return donation    
        
           
    # regra de negocio para buscar doação por id 
    def service_search_donations(self,donation_id:int):
        id = self.repository_donation.select_id_donation(donation_id)
        if not id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Doação não encontrada')
        
        donation = self.repository_donation.select_id_donation(donation_id)
        return donation      
    
    # regra de negocio para listar todas as doações do BD
    def service_list_donation(self):
        donation= self.repository_donation.list_donations()
        return donation
    
    
    #  regra de negocio para listar as doacoes por doador
    def service_get_donations_by_donor(self,donor_id:int,usuario_logado:User):
        donor = self.repository_donation.select_donor_id(donor_id)
        if not donor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Doador não exitente')
        
        if donor.donor_id != usuario_logado.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Você não possui essas doações')
        donations = self.repository_donation.get_donations_by_donor(donor.donor_id)
        return donations
    
    # regra de negocio para editar uma doação 
    def service_edit_donation(self,id:int,donation:Donation_simple,usuario_logado:User):
        buscar_id = self.repository_donation.select_id_donation(id)
        if not buscar_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Produto não encontrado')
        
        
        if buscar_id.donor_id != usuario_logado.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Você não possui esse produto')
        
        donation.donor_id = usuario_logado.id
        donation.id = id
        
        self.repository_donation.update_donation(id,donation)
        return donation
    
    
    def service_delete(self,donation_id:int, usuario_logado:User):
        donation = self.repository_donation.select_id_donation(donation_id)
        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Doação não encontrada')
        
        if donation.donor_id != usuario_logado.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Você não tem autorização para deletar essa doação')   
        
        try:
            self.repository_donation.delete_donation(donation_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f'Erro ao deletar a doação {e}')        
    