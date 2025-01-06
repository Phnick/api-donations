from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends,BackgroundTasks,status
# from infra.sqlalchemy.models.models import Usuario
from infra.sqlalchemy.repository.repository_user import RepositoryUser
from infra.providers import hash_providers,token_providers
from schemas.schemas import User,User_simple,Recover_password


class UserService:
    def __init__(self,db:Session):
        self.db = db
        self.repository_user = RepositoryUser(db)

    # create user
    def user_create(self,user:User,background_task :BackgroundTasks):
        if not user.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='error,campo name nao preenchido')    
        if not user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='error,campo email nao preenchido')
        if not user.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='error,campo password nao preenchido')
        
        localized_user = self.repository_user.get_email(user.email)  
        if localized_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='email ja cadastrado') 

        user.password = hash_providers.create_hash(user.password) 
        user_created = self.repository_user.create(user)  

        subject = 'Bem vindo/a ao nosso app de doações'
        body = f'Olá{user.email},\n\nSeu cadastro foi realizado com sucesso!' 
        background_task.add_task(self.repository_user.send_email,user.email,subject,body)

        return user_created 
    

    # show info user
    def show_user(self,user_id:int):
        user = self.repository_user.list_user(user_id)
        return user
    
    # edit info user
    def edit_user(self,user_update:User_simple,user_logged_in:User):
        if user_update.email != user_logged_in.email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Sem autorização')
        
        get_user = self.repository_user.get_email(user_update.email)
        if not get_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='usuario nao encontrado')
        
        try:
            self.repository_user.edit_user(user_update)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f'erro ao editar usuario{e}') 
        return user_update   
    

    # autentic user
    def autentic_user(self,password:str, email:str):
        if not password or not email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='email e senha são obrigatorios')
        
        user = self.repository_user.get_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='senha ou email incorretos')
        
        check_passwor= hash_providers.check_hash(password,user.password)
        if not check_passwor:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='senha ou email incorretos')
        
        token = token_providers.cerate_access_token({'sub': user.email})
        return user,token
    
    # delete user account
    def delete_user(self,id:int,user_logged_in:User):
        search_id = self.repository_user.get_id(id)
        if not search_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Id não encontrado')
        
        if search_id.id != user_logged_in.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='id diferente do id logado')
        
        try:
            self.repository_user.delete_user(id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f'Erro ao deletar usuario {e}')   
