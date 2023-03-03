from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify(secret_password, hashed_password):
    return pwd_context.verify(secret_password, hashed_password)
