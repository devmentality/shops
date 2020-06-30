from pydantic import BaseModel, EmailStr
from shops.schemas.base import OrmBaseSchema, NonEmptyStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    first_name: NonEmptyStr
    last_name: NonEmptyStr


class UserCreateSchema(UserBaseSchema):
    password: NonEmptyStr


class UserInfoSchema(UserBaseSchema, OrmBaseSchema):
    pass
