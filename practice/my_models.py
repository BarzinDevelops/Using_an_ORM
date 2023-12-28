#-------------------- ALL IMPORTS --------------------
from peewee import Model, CharField, DateField, ForeignKeyField
from my_database import db
#------------------- End of imports -------------------
class Person(Model):
    """ This part basically says "inherit all functionality from Model". 
    This adds all the querying functionality to the Person class, 
    allowing us to use something like Person.select() without having 
    to define a select method. 
    """
    name = CharField()
    birthday = DateField()
    
    class Meta:
        database = db # This model uses the "people.db" database.
        # if you want to use your own table name (otherwise class Person will be the name automatically!)
        # table_name = 'person_table'
        
class Pet(Model):
    owner_name = ForeignKeyField(Person, backref='pets')
    pet_name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # this model uses the "people.db" database

############# End Of All Operations #############    
if __name__ == "__main__":
    print(f"This module contains only MODELS."
    f"\nOnly to be imported and NOT to be executed!!")