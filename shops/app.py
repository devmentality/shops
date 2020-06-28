import jwt
from datetime import datetime, timedelta
from http import HTTPStatus
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from mongoengine import connect
from shops.models.user import User
from shops.schemas.user import UserCreateSchema, UserInfoSchema
from passlib.context import CryptContext


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

connect(
    db='shops',
    host='mongodb://mongo',
    port=27017
)

SECRET_KEY = 'not_secret_at_all'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_MINUTES = 7 * 24 * 60


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


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    return create_jwt_access_token(user)


@app.get("/")
def index():
    return {"message": "Hello, world!"}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserInfoSchema)
def create_user(user_schema: UserCreateSchema):
    password_hash = get_password_hash(user_schema.password)

    user_dict = user_schema.dict()
    del user_dict['password']
    user_dict['password_hash'] = password_hash

    user = User(**user_dict).save()
    return UserInfoSchema.from_orm(user)


@app.get('/users/me', response_model=UserInfoSchema)
def get_all_users(user: User = Depends(get_current_user)):
    return UserInfoSchema.from_orm(user)
