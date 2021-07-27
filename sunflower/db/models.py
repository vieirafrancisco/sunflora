from peewee import Model, TextField, CharField

from sunflower.db import db


class BaseModel(Model):
    class Meta:
        database = db.db


class Product(BaseModel):
    name = CharField()
    url = TextField()


class Review(BaseModel):
    pass
