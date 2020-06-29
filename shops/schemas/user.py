from pydantic import BaseModel
from shops.schemas.base import OrmBaseSchema


class UserBaseSchema(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserInfoSchema(UserBaseSchema, OrmBaseSchema):
    pass
