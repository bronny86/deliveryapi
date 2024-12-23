from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.menu_item import MenuItem, menu_item_schema, menu_items_schema

menu_items_bp = Blueprint("menu_items", __name__, url_prefix="/menu_items")

# read all - /menu_items GET
@menu_items_bp.route("/")
def get_menu_items():
    stmt = db.select(MenuItem)
    menu_items_list = db.session.scalars(stmt)
    data = menu_items_schema.dump(menu_items_list)
    return data

# read one - /menu_items/id - GET
@menu_items_bp.route("/<int:menu_item_id>")
def get_menu_item(menu_item_id):
    stmt = db.select(MenuItem).filter_by(id=menu_item_id)
    menu_item = db.session.scalar(stmt)
    if menu_item:
        data = menu_item_schema.dump(menu_item)
        return data
    else:
        return {"message": f"Menu item with id {menu_item_id} does not exist"}, 404

# create - /menu_items - POST
@menu_items_bp.route("/", methods=["POST"])
def create_menu_item():
    try:
        body_data = menu_item_schema.load(request.get_json())
        new_menu_item = MenuItem(
            name=body_data.get("name"),
            price=body_data.get("price"),
            restaurant_id=body_data.get("restaurant_id")
        )
        db.session.add(new_menu_item)
        db.session.commit()
        return menu_item_schema.dump(new_menu_item), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} cannot be null"}, 409

# delete - /menu_items/id - DELETE
@menu_items_bp.route("/<int:menu_item_id>", methods=["DELETE"])
def delete_menu_item(menu_item_id):
    stmt = db.select(MenuItem).where(MenuItem.id == menu_item_id)
    menu_item = db.session.scalar(stmt)
    if menu_item:
        db.session.delete(menu_item)
        db.session.commit()
        return {"message": f"Menu item with id {menu_item_id} deleted"}
    else:
        return {"message": f"Menu item with id {menu_item_id} does not exist"}, 404

# update - /menu_items/id - PUT
@menu_items_bp.route("/<int:menu_item_id>", methods=["PUT"])
def update_menu_item(menu_item_id):
    stmt = db.select(MenuItem).filter_by(id=menu_item_id)
    menu_item = db.session.scalar(stmt)
    if menu_item:
        body_data = menu_item_schema.load(request.get_json())
        menu_item.name = body_data.get("name") or menu_item.name
        menu_item.price = body_data.get("price") or menu_item.price
        menu_item.restaurant_id = body_data.get("restaurant_id") or menu_item.restaurant_id
        return menu_item_schema.dump(menu_item)
    else:
        return {"message": f"Menu item with id {menu_item_id} does not exist"}, 404

