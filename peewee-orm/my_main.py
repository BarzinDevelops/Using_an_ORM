#-------------------- ALL IMPORTS --------------------
from my_functions import *
from my_database import db
#------------------- End of imports -------------------


def main():
    create_tables()
    create_person(name="Jimmy", birthday="01-01-1980")
    create_person(name="Helena", birthday="23-11-1986")
    create_person(name="Mika", birthday="21-12-1984")
    create_person(name='John', birthday='1990-01-01')
    create_person(name='Jane', birthday='1985-05-15')

    create_pet(owner_name="Jimmy", pet_name='Fluffy', animal_type='Cat')
    create_pet(owner_name="Helena", pet_name='Buddy', animal_type='Dog')
    create_pet(owner_name="Mika", pet_name='Whiskers', animal_type='Cat')
    create_pet(owner_name="Jane", pet_name='Max', animal_type='Dog')
    
############# End Of All Operations #############    
if __name__ == "__main__":
    main()