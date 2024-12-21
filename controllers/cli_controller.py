from flask import Blueprint

from init import db
from models.customer import Customer


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
        
    db.session.commit()
    
    print("Tables seeded")