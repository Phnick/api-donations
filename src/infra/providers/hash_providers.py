from passlib.context import CryptContext


# aqui e o hashing de senhas
# pwd_context = CryptContext(schemes='argon2')
pwd_context = CryptContext(schemes='bcrypt')
# pwd_context = CryptContext(schemes=["argon2", "bcrypt"])


def create_hash(text):
    return pwd_context.hash(text)


def check_hash(texto,hash):
    return pwd_context.verify(texto,hash)