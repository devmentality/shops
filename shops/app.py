from http import HTTPStatus
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from mongoengine import connect
from shops.auth import (
    get_current_user, get_password_hash, authenticate_user, create_jwt_access_token
)
from shops.models.user import User
from shops.models.shop import Shop
from shops.models.product import Product
from shops.schemas.user import UserCreateSchema, UserInfoSchema
from shops.schemas.shop import ShopBaseSchema, ShopInfoSchema
from shops.schemas.product import ProductBaseSchema, ProductInfoSchema


app = FastAPI()

connect(
    db='shops',
    host='mongodb://mongo',
    port=27017
)


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    return create_jwt_access_token(user)


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserInfoSchema)
def create_user(user_schema: UserCreateSchema):
    password_hash = get_password_hash(user_schema.password)

    user_dict = user_schema.dict()
    del user_dict['password']
    user_dict['password_hash'] = password_hash

    user = User(**user_dict).save()
    return UserInfoSchema.from_orm(user)


@app.get('/users/me', response_model=UserInfoSchema)
def get_all_users(user: User = Depends(get_current_user)):
    return UserInfoSchema.from_orm(user)


@app.post('/shops', status_code=HTTPStatus.CREATED, response_model=ShopInfoSchema)
def create_shop(shop_schema: ShopBaseSchema, user: User = Depends(get_current_user)):
    shop = Shop(**shop_schema.dict())
    shop.owner = user
    shop.save()

    return ShopInfoSchema.from_orm(shop)


@app.post('/shops/my')
def get_user_shops(user: User = Depends(get_current_user)):
    return {'shops':
            [ShopInfoSchema.from_orm(shop)
                for shop in Shop.objects(owner=user).all()]
            }


@app.post('/shops/{shop_id}/products', status_code=HTTPStatus.CREATED, response_model=ProductInfoSchema)
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
