from mongoengine import *
from shops.models.shop import Shop


class Product(Document):
    name = StringField(required=True)
    description = StringField()
    price = DecimalField()
    categories = ListField(StringField())
    shop = ReferenceField(Shop, reverse_delete_rule=CASCADE)
