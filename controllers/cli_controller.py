from flask import Blueprint

from init import db
from models.customer import Customer
from models.dasher import Dasher
from models.restaurant import Restaurant

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")  
def create_db():
    db.create_all()
    print("Tables created")
    
@db_commands.cli.command("drop")    
def drop_db():
    db.drop_all()
    print("Tables dropped")
    
@db_commands.cli.command("seed")
def seed_tables():
    customers = [
        Customer(
            name="Minky Binky",
            address="1234 5th Street",
            phone="123-456-7890"
        ),
        Customer(
            name="Dan Watt",
            address="1234 6th Street",
            phone="123-456-7800"
        )
    ]
   
    db.session.add_all(customers)
    
    dashers = [
        Dasher(
            name="Honey",
            phone="2356335",
            email="honey@puppy.com"
        ),
        Dasher(
            name="Bunny",
            phone="23564336",
            email="bunny@kitten.com"
        )
    ]
    
    db.session.add_all(dashers)
    
    restaurants = [
        Restaurant(
            name="McDonalds",
            address="1234 7th Street",
            cuisine="Fast Food",
            phone="123-456-7890"
        ),
        Restaurant(
            name="Smoking Joes",
            address="1234 8th Street",
            cuisine="Italian",
            phone="123-456-7800"
        ),
        
        Restaurant(
            name="Taco Bell",
            address="1234 9th Street",
            cuisine="Mexican",
            phone="123-456-7890"
        ),
        Restaurant(
            name="Panda Express",
            address="1234 10th Street",
            cuisine="Chinese",
            phone="123-456-7800"
        ),
        Restaurant(
            name="Dosa Hut",
            address="1234 11th Street",
            cuisine="Indian",
            phone="123-456-7890"
        )
    ]
    
    db.session.add_all(restaurants)
        
    db.session.commit()
    
    print("Tables seeded")