from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from shops.auth import get_current_user
from shops.models.user import User
from shops.models.shop import Shop
from shops.models.product import Product
from shops.schemas.shop import ShopBaseSchema, ShopInfoSchema
from shops.schemas.product import ProductBaseSchema, ProductInfoSchema

router = APIRouter()


@router.post('/shops', status_code=HTTPStatus.CREATED, response_model=ShopInfoSchema)
def create_shop(shop_schema: ShopBaseSchema, user: User = Depends(get_current_user)):
    shop = Shop(**shop_schema.dict())
    shop.owner = user
    shop.save()

    return ShopInfoSchema.from_orm(shop)


@router.post('/shops/my')
def get_user_shops(user: User = Depends(get_current_user)):
    return {'shops':
            [ShopInfoSchema.from_orm(shop)
                for shop in Shop.objects(owner=user).all()]
            }


@router.post('/shops/{shop_id}/products', status_code=HTTPStatus.CREATED, response_model=ProductInfoSchema)
def create_product(
        shop_id: str,
        product_schema: ProductBaseSchema,
        user: User = Depends(get_current_user)):
    shop = Shop.objects(id=shop_id).first()
    if shop is None or shop.owner != user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Shop is not found or you have no permission"
        )

    product = Product(**product_schema.dict())
    product.shop = shop
    product.save()

    return ProductInfoSchema.from_orm(product)
