from http import HTTPStatus
from fastapi import FastAPI
from mongoengine import connect
from shops.models.user import User
from shops.schemas.user import UserBaseSchema, UserInfoSchema


app = FastAPI()

connect(
    db='shops',
    host='mongodb://mongo',
    port=27017
)


@app.get("/")
def index():
    return {"message": "Hello, world!"}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserInfoSchema)
def create_user(user_schema: UserBaseSchema):
    user = User(**user_schema.dict()).save()
    return UserInfoSchema.from_orm(user)
