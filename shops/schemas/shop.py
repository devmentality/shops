from pydantic import BaseModel
from shops.schemas.base import OrmBaseSchema


class ShopBaseSchema(BaseModel):
    name: str


class ShopInfoSchema(ShopBaseSchema, OrmBaseSchema):
    pass
