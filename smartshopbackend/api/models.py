from django.db import models
from mongoengine import Document, fields
from datetime import datetime, timedelta
import uuid

class Catagory(Document):
    name = fields.StringField(max_length=50, required=True)
    

class Product(Document):
    name = fields.StringField(max_length=50, required=True)
    price = fields.IntField(required=True)
    catagory = fields.ReferenceField(Catagory, required=True)
    description = fields.StringField(max_length=200, required=True)


class User(Document):
    user = fields.StringField(required= True, max_length=50)
    email = fields.StringField(required=True, max_length=60)
    password = fields.StringField(required=True, max_length=70)

class AuthToken(Document):
    user = fields.StringField(required= True, max_length=50)
    token = fields.StringField(default = lambda : str(uuid.uuid4()), unique=True)
    created_at = fields.DateTimeField(default=datetime.now)

    def is_valid(self):
        return datetime.now() - self.created_at < timedelta(days=1)


class CartItem(Document):
    user = fields.StringField(required=True)
    products= fields.ReferenceField(Product, required=True)
    quantity= fields.IntField(required=True)

    def get_total(self, price):
        return self.quantity * price




    

    
