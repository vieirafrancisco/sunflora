from peewee import (
    Model, TextField, CharField,
    ForeignKeyField, BooleanField,
    IntegerField, FloatField
)

from sunflower.db import Database

db = Database().db

class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    name = CharField()
    initials = CharField()
    url = CharField(unique=True)
    parent = ForeignKeyField("self", related_name="children", null=True)

    class Meta:
        indexes = (
            (("name", "initials"), True),
        )

    def __str__(self):
        return f"Category: {self.name} ({self.initials})"


class Product(BaseModel):
    name = CharField()
    url = TextField(unique=True)

    def __str__(self):
        return f"Product ({self.name})"


class ProductCategory(BaseModel):
    product = ForeignKeyField(Product)
    category = ForeignKeyField(Category)


class Review(BaseModel):
    rating = FloatField()
    username = CharField()
    relative_data = CharField()
    title = CharField()
    text = TextField()
    is_recommended = BooleanField()
    thumbs_up = IntegerField()
    thumbs_down = IntegerField()
    cost_benefit_rate = FloatField()
    general_quality_rate = FloatField()

models_list = [Product, Category, ProductCategory, Review]
