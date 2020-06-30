from pydantic import BaseModel
from shops.schemas.base import OrmBaseSchema, NonEmptyStr


class ShopBaseSchema(BaseModel):
    name: NonEmptyStr


class ShopInfoSchema(ShopBaseSchema, OrmBaseSchema):
    pass
