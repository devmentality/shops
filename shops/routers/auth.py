from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from shops.auth import authenticate_user, create_jwt_access_token

router = APIRouter()


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    return create_jwt_access_token(user)
