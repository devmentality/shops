from pydantic import BaseModel, validator, constr


class OrmBaseSchema(BaseModel):
    id: str

    @validator('id', pre=True)
    def id_to_str(cls, value):
        return str(value)

    class Config:
        orm_mode = True


NonEmptyStr = constr(strip_whitespace=True, min_length=1)
