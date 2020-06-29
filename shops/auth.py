import jwt
from datetime import datetime, timedelta
from http import HTTPStatus
from passlib.context import CryptContext
from shops.models.user import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'not_secret_at_all'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = 7 * 24 * 60

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


def get_password_hash(password: str):
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def authenticate_user(user_email: str, user_password: str) -> User:
    user = User.objects(email=user_email).first()
    if user and verify_password(user_password, user.password_hash):
        return user

    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"}
    )


def create_jwt_access_token(user: User):
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES),
        "sub": user.email
    }
    return {
        "access_token": jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer"
    }


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise credentials_exception

    user_email = payload['sub']
    user = User.objects(email=user_email).first()
    if user is None:
        raise credentials_exception
    return user
