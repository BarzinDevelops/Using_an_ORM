from peewee import SqliteDatabase

""" To connect to a SQLite database, we will use SqliteDatabase. 
The first parameter is the filename containing the database, 
or the string ':memory:' to create an in-memory database.  
"""
db = SqliteDatabase('people_and_pets.db') # instead of 'people.db' -> use ':memory:' to create an in-memory database. 


############# End Of All Operations #############    
if __name__ == "__main__":
    print(f"This module contains only database related functions and variables."
    f"\nOnly to be imported and NOT to be executed!!")