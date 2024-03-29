import peewee


# db = peewee.SqliteDatabase("../database.db")
db = peewee.SqliteDatabase(":memory:")

class Ingredient(peewee.Model):
    name = peewee.CharField()
    is_vegetarian = peewee.BooleanField()
    is_vegan = peewee.BooleanField()
    is_glutenfree = peewee.BooleanField()

    class Meta:
        database = db


class Restaurant(peewee.Model):
    name = peewee.CharField()
    open_since = peewee.DateField()
    opening_time = peewee.TimeField(formats=["%H:%M"])
    closing_time = peewee.TimeField(formats=["%H:%M"])

    class Meta:
        database = db


class Dish(peewee.Model):
    name = peewee.CharField()
    served_at = peewee.ForeignKeyField(Restaurant)
    price_in_cents = peewee.DecimalField(decimal_places=2)
    ingredients = peewee.ManyToManyField(Ingredient)

    class Meta:
        database = db


class Rating(peewee.Model):
    restaurant = peewee.ForeignKeyField(Restaurant)
    rating = peewee.IntegerField()
    comment = peewee.CharField(null=True)

    class Meta:
        database = db


DishIngredient = Dish.ingredients.get_through_model()


