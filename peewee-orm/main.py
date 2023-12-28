import models
from models import db
from peewee import fn, JOIN
from typing import List

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def adding_dish():
    # Define a dish to add
    dishes_to_add = [
        {"name": "Taboule", "served_at": 5, "price_in_cents": 1350},
        {"name": "spaghetti bolognese", "served_at": 5, "price_in_cents": 1680},
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
        else:
            # Create and add the new dish
            new_dish = models.Dish.create(name=dish["name"], served_at=dish["served_at"], price_in_cents=dish["price_in_cents"])
            print(f"New dish added successfully. Dish ID: {new_dish.id}")

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
    add_rating_to_restaurant()
     
     
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
    restaurant = models.Restaurant.get_by_id(5)
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
    ...


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    ...



if __name__ == "__main__":
    tester()