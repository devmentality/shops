from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from shops.auth import get_password_hash, get_current_user
from shops.models.user import User
from shops.schemas.user import UserCreateSchema, UserInfoSchema

router = APIRouter()


@router.post('/users', status_code=HTTPStatus.CREATED, response_model=UserInfoSchema)
def create_user(user_schema: UserCreateSchema):
    user_exists = User.objects(email=user_schema.email).exists()
    if user_exists:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User with this email already exists"
        )

    password_hash = get_password_hash(user_schema.password)

    user_dict = user_schema.dict()
    del user_dict['password']
    user_dict['password_hash'] = password_hash

    user = User(**user_dict).save()
    return UserInfoSchema.from_orm(user)


@router.get('/users/me', response_model=UserInfoSchema)
def get_all_users(user: User = Depends(get_current_user)):
    return UserInfoSchema.from_orm(user)
