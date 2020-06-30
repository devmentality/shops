from pydantic import BaseModel
from decimal import Decimal
from typing import List
from shops.schemas.base import OrmBaseSchema, NonEmptyStr


class ProductBaseSchema(BaseModel):
    name: NonEmptyStr
    description: str
    price: Decimal
    categories: List[str]


class ProductInfoSchema(ProductBaseSchema, OrmBaseSchema):
    pass
