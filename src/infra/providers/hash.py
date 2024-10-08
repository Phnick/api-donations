from passlib.context import CryptContext



pwd_context = CryptContext(schemes='bcrypt')


def create_hash(text):
    return pwd_context.hash(text)


def check_hash(texto,hash):
    return pwd_context.verify(texto,hash)