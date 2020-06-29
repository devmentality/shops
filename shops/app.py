from fastapi import FastAPI
from mongoengine import connect
from shops.routers import auth, shops, users

app = FastAPI()

connect(
    db='shops',
    host='mongodb://mongo',
    port=27017
)

app.include_router(auth.router)
app.include_router(shops.router)
app.include_router(users.router)
