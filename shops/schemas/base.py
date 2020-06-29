from pydantic import BaseModel, validator


class OrmBaseSchema(BaseModel):
    id: str

    @validator('id', pre=True)
    def id_to_str(cls, value):
        return str(value)

    class Config:
        orm_mode = True