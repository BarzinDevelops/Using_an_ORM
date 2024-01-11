import models
from models import db
from peewee import fn, JOIN
from typing import List
from datetime import datetime as dt, time

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"




def tester():
    """ 
    query = (models.Dish
             .select(models.Dish, models.Restaurant.name.alias(alias='rest_name'))
             .join(models.Restaurant, on=(models.Dish.served_at == models.Restaurant.id)))
    print(f"dish_id\t\tname\t\t\tserved_at_id\tprice_in_cents\t\trestaurant_name")
    for row in query.objects():       
        print(f"\t{row.id}\t\t{row.name}\t\t{row.served_at_id}\t\t{row.price_in_cents}\t\t{row.rest_name}\t")
     """
    # adding_dish()
    # dinner_date_possible()
    print(add_dish_to_menu())
    # ingredient = models.Ingredient.get_or_none(models.Ingredient.name ** 'sosis')
    # print(f"Test: ingredient = {ingredient}")
     
def cheapest_dish() -> models.Dish:
    """You want ot get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    cheapest_dish_found = models.Dish.select().order_by(models.Dish.price_in_cents).first()
    return cheapest_dish_found

def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """
    is_vegetarian_dish = None
    
    # step1: get all the dishes:
    all_dishes = models.Dish.select()
    
    # Step 2 & 3: Check if ingredients are vegetarian:
    vegetarian_dishes = []
    for dish in all_dishes:      
        is_vegetarian_dish = all(ingredient.is_vegetarian for ingredient in dish.ingredients)    
        if is_vegetarian_dish:
            vegetarian_dishes.append(dish)       
    print(f"is_vegetarian_dish  => {is_vegetarian_dish}")
    return vegetarian_dishes

def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """   
    # Select restaurants and calculate the average rating for each
    best_rated_restaurant = (models.Restaurant
             .select(models.Restaurant, fn.AVG(models.Rating.rating).alias('avg_rating'))
             .join(models.Rating, JOIN.LEFT_OUTER, on=(models.Restaurant.id == models.Rating.restaurant))
             .group_by(models.Restaurant)
             .order_by(fn.AVG(models.Rating.rating).desc())
             .limit(1))

    return best_rated_restaurant.first()

def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating

    Select the first restaurant in the dataset and add a rating
    """
    restaurant = models.Restaurant.get_by_id(3)
    print(f"restaurant reference: {restaurant}\n Restaurant name: {restaurant.name}")
    # create a new rating:
    new_rating_instance = {'restaurant': restaurant, 'rating': 4, 'comment': 'Very chill place and nice service.'}
    
    new_rating = models.Rating.create(**new_rating_instance)
    
    print(f"Rating added successfully for restaurant: '{restaurant.name}'."
          f"Rating ID: {new_rating.id}")




def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?
    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """
        
    # time constraint (around 19:00)
    desired_time = time(19, 0)    
    #  Query for restaurants that are open around the desired time and serve vegan food
    restaurants = (
        models.Restaurant.select()
        .where(models.Restaurant.opening_time <= "19:00") 
        .where(models.Restaurant.closing_time >= "19:00")   
    )
    title_seperator = '=='*20
    dish_seperator = '--'*15
    restaurant_list = []
    for restaurant in restaurants:
        # print(f"\n{title_seperator}\n restaurant : {restaurant.name} \n{title_seperator}\n")
        for dish in restaurant.dish_set.select():
            # print(f"\n{dish_seperator}\ndish : {dish.name}\n{dish_seperator}\n")
            ingredient_list = []
            for ingredient in dish.ingredients:
                # print(f"{'VEGAN - 'if ingredient.is_vegan else 'NOT VEGAN - '}"
                    #   f"ingredient : {ingredient.name}")
                ingredient_list.append(ingredient.is_vegan)
            if all(ingredient_list):
                restaurant_list.append(restaurant)
    # print(f"\n\nrestaurant with vegan food: {restaurant.name}\nwith id: {restaurant.id}")
    return restaurant_list

def add_dish(dish_name, restaurant_id, price_in_cents):
    # Define a dish to add
    dishes_to_add = [
        {"name": dish_name, "served_at": restaurant_id, "price_in_cents": price_in_cents},
    ]
    
    for dish in dishes_to_add:
        # Check if a dish with the same name already exists
        existing_dish = models.Dish.select() \
                        .where(
                            (models.Dish.name == dish["name"]) & 
                            (models.Dish.served_at == dish["served_at"])
                        ).first()

        if existing_dish:
            print(f"Dish with the name '{dish['name']}' already exists.")
            return existing_dish
        else:
            # Create and add the new dish
            new_dish = models.Dish.create(name=dish["name"], served_at=dish["served_at"], price_in_cents=dish["price_in_cents"])
            print(f"New dish: {new_dish.name} added successfully. Dish ID: {new_dish.id}")
            return new_dish
        
def add_ingredients(name, is_vegetarian, is_vegan, is_glutenfree):
    # Check if the ingredient with the same name already exists
    existing_ingredient = models.Ingredient.get_or_none(models.Ingredient.name == name)
    if existing_ingredient:
        print(f"This ingredient: '{existing_ingredient.name}' already exists.")
        return existing_ingredient
    else:
        # Create and add the new dish
        new_ingredient = models.Ingredient.create(name=name, is_vegetarian=is_vegetarian, is_vegan=is_vegan, is_glutenfree=is_glutenfree)
        print(f"New ingredient: {new_ingredient.name} added successfully."
              f"Ingredient ID: {new_ingredient.id}")
        return new_ingredient



def add_ingredient_to_dish_ingredient(new_ingredients_objects_list, dish):
    # Retrieve the DishIngredient through model
    DishIngredient = models.Dish.ingredients.get_through_model()

    for new_ingredient in new_ingredients_objects_list:
        # Check if the DishIngredient already exists for the given dish and ingredient
        existing_dish_ingredient = DishIngredient.select().where(
            (DishIngredient.dish_id == dish.id) &
            (DishIngredient.ingredient_id == new_ingredient.id)
        ).first()

        if existing_dish_ingredient:
            print(f"This ingredient: '{new_ingredient.name}' is already related to the dish: {dish.name}. DishIngredient ID: {existing_dish_ingredient.id}")
        else:
            # Create the DishIngredient relationship
            added_ingredient = DishIngredient.create(
                dish_id=dish.id,
                ingredient_id=new_ingredient.id
            )
            print(f"New ingredient: {new_ingredient.name} is now related successfully to the dish: {dish.name} with DishIngredient ID: {added_ingredient.id}.")


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    
    # new_dish =models.Dish.create(name='barrychello', served_at=5, price_in_cents=3800)
    # new_dish.save()
    print(f"============ add_dish_to_menu =============\n")
    
    """ # if you want an instance of an existing dish
    dish_to_add = 'some_dish_name'
    
    existing_dish = models.Dish.get_or_none(models.Dish.name == dish_to_add)
    if existing_dish:
        print(f"existing_dish: {existing_dish.name} and ID: {existing_dish.id}\n")
    else:
        print(f"'{dish_to_add}' -> doesn't exist yet in 'models.Dish'.\n"
              f"At this moment -> 'existing_dish' contains: {existing_dish}\n")
    """
    # if new dish is added you get it's instance like following:
    added_dish = add_dish(dish_name='barrychello', restaurant_id=4, price_in_cents=3800)
    print(f"added_dish Name: {added_dish.name} and ID: {added_dish.id}")
    
    bread = add_ingredients(name='bread', is_vegetarian=True, is_vegan=True, is_glutenfree=False)
    tomato = add_ingredients(name='tomato', is_vegetarian=True, is_vegan=True, is_glutenfree=True)
    cheese = add_ingredients(name='cheese', is_vegetarian=True, is_vegan=False, is_glutenfree=True)
    sosis = add_ingredients(name='sosis', is_vegetarian=False, is_vegan=False, is_glutenfree=True)
    kalbas = add_ingredients(name='kalbas', is_vegetarian=False, is_vegan=False, is_glutenfree=True)

    new_ingredients = [bread, tomato, cheese, sosis, kalbas]
    print(f"new_ingredients: {new_ingredients}")
    
    add_ingredient_to_dish_ingredient(new_ingredients, added_dish)

    return added_dish

if __name__ == "__main__":
    tester()