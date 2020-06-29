from pydantic import BaseModel
from decimal import Decimal
from typing import List
from shops.schemas.base import OrmBaseSchema


class ProductBaseSchema(BaseModel):
    name: str
    description: str
    price: Decimal
    categories: List[str]


class ProductInfoSchema(ProductBaseSchema, OrmBaseSchema):
    pass
