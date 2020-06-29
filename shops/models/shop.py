from mongoengine import Document, StringField, ReferenceField, CASCADE
from shops.models.user import User


class Shop(Document):
    name = StringField(required=True)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
