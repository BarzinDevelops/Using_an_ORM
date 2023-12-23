#-------------------- ALL IMPORTS --------------------
from my_database import db 
from my_models import Person, Pet
#------------------- End of imports -------------------
# =====================================================
# Create operations
# =====================================================
def create_tables():
    with db:
        db.create_tables([Person, Pet])

def create_person(name, birthday):
    with db.atomic():
        existing_object = Person.get_or_none(name=name)
        # Create a new person if not found
        if not existing_object:
            person = Person.create(name=name, birthday=birthday)
             # Print the values of the fields in the returned person object
            print(f"Created person: "
                  f"ID={person.id}, "
                  f"Name={person.name}, "
                  f"Birthday={person.birthday}")
        else:
            print(f"This person: '{existing_object.name}', already exists!")
            
def create_pet(owner_name, pet_name, animal_type):
    with db.atomic():
        found_owner = Person.get_or_none(name=owner_name)
        
        if found_owner:
            existing_object = Pet.get_or_none(pet_name=pet_name)
            if not existing_object:
                pet = Pet.create(owner_name=found_owner, pet_name=pet_name, animal_type=animal_type)
                print(f"Created pet: "
                    f"ID={pet.id}, "
                    f"Owner={pet.owner_name}, "
                    f"Name={pet.pet_name}, "
                    f"animal type={pet.animal_type}")
            else:
                print(f"This pet: '{existing_object.pet_name}', already exists!")
        else:
            print(f"No person found with name: '{owner_name}'")
# __________End of Create operations_____________________
    
# =====================================================
# Read operations
# =====================================================

# __________End of Read operations_____________________
# =====================================================
# Update operations
# =====================================================


# __________End of Update operations_____________________
# =====================================================
# Delete operations
# =====================================================


# __________End of Delete operations_____________________

#################### End Of All Operations ##########################
if __name__ == "__main__":
    print(f"This module contains only functions."
          f"\nOnly to be imported and NOT to be executed!!")