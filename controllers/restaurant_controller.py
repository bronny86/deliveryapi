from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.restaurant import Restaurant, restaurant_schema, restaurants_schema

restaurants_bp = Blueprint("restaurants", __name__, url_prefix="/restaurants")

# read all - /restaurants GET
@restaurants_bp.route("/")
def get_restaurants():
    stmt = db.select(Restaurant)
    restaurants_list = db.session.scalars(stmt)
    data = restaurants_schema.dump(restaurants_list)
    return data

# read one - /restaurants/id - GET
@restaurants_bp.route("/<int:restaurant_id>")
def get_restaurant(restaurant_id):
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        data = restaurant_schema.dump(restaurant)
        return data
    else:
        return {"message": f"Restaurant with id {restaurant_id} does not exist"}, 404

# create - /restaurants - POST
@restaurants_bp.route("/", methods=["POST"])
def create_restaurant():
    try:
        body_data = restaurant_schema.load(request.get_json())
        new_restaurant = Restaurant(
            name=body_data.get("name"),
            address=body_data.get("address"),
            cuisine=body_data.get("cuisine"),
            phone=body_data.get("phone")
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return restaurant_schema.dump(new_restaurant), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} cannot be null"}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Phone number already in use"}, 409

# delete - /restaurants/id - DELETE
@restaurants_bp.route("/<int:restaurant_id>", methods=["DELETE"])
def delete_restaurant(restaurant_id):
    stmt = db.select(Restaurant).where(Restaurant.id == restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {"message": f"Restaurant with id {restaurant_id} deleted"}
    else:
        return {"message": f"Restaurant with id {restaurant_id} does not exist"}, 404

# update - /restaurants/id - PUT
@restaurants_bp.route("/<int:restaurant_id>", methods=["PUT", "PATCH"])
def update_restaurant(restaurant_id):
    stmt = db.select(Restaurant).filter_by(id=restaurant_id)
    restaurant = db.session.scalar(stmt)
    if restaurant:
        try:
            body_data = restaurant_schema.load(request.get_json())
            restaurant.name = body_data.get("name") or restaurant.name
            restaurant.address = body_data.get("address") or restaurant.address
            restaurant.cuisine = body_data.get("cuisine") or restaurant.cuisine
            restaurant.phone = body_data.get("phone") or restaurant.phone
            db.session.commit()
            return restaurant_schema.dump(restaurant)
        except IntegrityError as err:
            if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {"message": f"The field {err.orig.diag.column_name} cannot be null"}, 409
            
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {"message": "Phone number already in use"}, 409
    else:
        return {"message": f"Restaurant with id {restaurant_id} does not exist"}, 404