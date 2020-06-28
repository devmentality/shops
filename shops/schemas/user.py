from pydantic import BaseModel, validator


class UserBaseSchema(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserInfoSchema(UserBaseSchema):
    id: str

    @validator('id', pre=True)
    def id_to_str(cls, value):
        return str(value)

    class Config:
        orm_mode = True
