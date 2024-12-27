from flask import Blueprint

from init import db
from models.customer import Customer
from models.dasher import Dasher
from models.restaurant import Restaurant
from models.order import Order
from models.menu_item import MenuItem
from models.order_item import OrderItem

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
    
    db.session.commit()
    
    restaurants = [
        Restaurant(
            name="McDonalds",
            address="1234 7th Street",
            cuisine="Fast Food",
            phone="123-456-7891"
        ),
        Restaurant(
            name="Smoking Joes",
            address="1234 8th Street",
            cuisine="Italian",
            phone="123-456-782"
        ),
        
        Restaurant(
            name="Taco Bell",
            address="1234 9th Street",
            cuisine="Mexican",
            phone="123-456-7490"
        ),
        Restaurant(
            name="Panda Express",
            address="1234 10th Street",
            cuisine="Chinese",
            phone="123-456-7600"
        ),
        Restaurant(
            name="Dosa Hut",
            address="1234 11th Street",
            cuisine="Indian",
            phone="123-456-7896"
        )
    ]
    
    db.session.add_all(restaurants)
    
    db.session.commit()
    
    orders = [
        Order(
            order_date="2024-12-23",
            order_total=23.45,
            delivery_address="1234 12th Street",
            customer_id=customers[0].id,
            dasher_id=dashers[0].id
        ),
        Order(
            order_date="2024-12-23",
            order_total=24.45,
            delivery_address="1234 13th Street",
            customer_id=customers[1].id,
            dasher_id=dashers[1].id)
    ]
    
    db.session.add_all(orders)
    
    db.session.commit()
    
    menu_items = [
        MenuItem(
            name="Big Mac",
            price=5.99,
            restaurant_id=restaurants[0].id
        ),
        MenuItem(
            name="Cheeseburger",
            price=1.99,
            restaurant_id=restaurants[0].id
        ),
        MenuItem(
            name="Spaghetti",
            price=10.99,
            restaurant_id=restaurants[1].id
        ),
        MenuItem(
            name="Lasagna",
            price=12.99,
            restaurant_id=restaurants[1].id
        ),
        MenuItem(
            name="Taco",
            price=2.99,
            restaurant_id=restaurants[2].id
        ),
        MenuItem(
            name="Burrito",
            price=4.99,
            restaurant_id=restaurants[2].id
        ),
        MenuItem(
            name="Orange Chicken",
            price=6.99,
            restaurant_id=restaurants[3].id
        ),
        MenuItem(
            name="Fried Rice",
            price=5.99,
            restaurant_id=restaurants[3].id
        ),
        MenuItem(
            name="Dosa",
            price=8.99,
            restaurant_id=restaurants[4].id
        ),
        MenuItem(
            name="Biryani",
            price=10.99,
            restaurant_id=restaurants[4].id
        )
    ]
    
    db.session.add_all(menu_items)
        
    db.session.commit()
    
    order_items = [
        OrderItem(
            quantity=2,
            order_id=orders[0].id,
            menu_item_id=menu_items[0].id
        ),
        OrderItem(
            quantity=1,
            order_id=orders[0].id,
            menu_item_id=menu_items[1].id
        ),
        OrderItem(
            quantity=3,
            order_id=orders[1].id,
            menu_item_id=menu_items[2].id
        ),
        OrderItem(
            quantity=2,
            order_id=orders[1].id,
            menu_item_id=menu_items[3].id
        ),
        OrderItem(
            quantity=4,
            order_id=orders[1].id,
            menu_item_id=menu_items[4].id
        ),
        OrderItem(
            quantity=2,
            order_id=orders[1].id,
            menu_item_id=menu_items[5].id
        ),
        OrderItem(
            quantity=3,
            order_id=orders[1].id,
            menu_item_id=menu_items[6].id
        ),
        OrderItem(
            quantity=2,
            order_id=orders[1].id,
            menu_item_id=menu_items[7].id
        ),
        OrderItem(
            quantity=1,
            order_id=orders[1].id,
            menu_item_id=menu_items[8].id
        ),
        OrderItem(
            quantity=1,
            order_id=orders[1].id,
            menu_item_id=menu_items[9].id
        )
    ]
    
    db.session.add_all(order_items)
    
    db.session.commit()
    
    print("Tables seeded")