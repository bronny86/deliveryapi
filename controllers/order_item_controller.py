from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.order_item import OrderItem, order_item_schema, order_items_schema

order_items_bp = Blueprint("order_items", __name__, url_prefix="/order_items")

# read all - /order_items GET
@order_items_bp.route("/")
def get_order_items():
    stmt = db.select(OrderItem)
    order_items_list = db.session.scalars(stmt)
    data = order_items_schema.dump(order_items_list)
    return data

# read one - /order_items/id - GET
@order_items_bp.route("/<int:order_item_id>")
def get_order_item(order_item_id):
    stmt = db.select(OrderItem).filter_by(id=order_item_id)
    order_item = db.session.scalar(stmt)
    if order_item:
        data = order_item_schema.dump(order_item)
        return data
    else:
        return {"message": f"OrderItem with id {order_item_id} does not exist"}, 404

# create - /order_items - POST
@order_items_bp.route("/", methods=["POST"])
def create_order_item():
    try:
        body_data = order_item_schema.load(request.get_json())
        new_order_item = OrderItem(
            quantity=body_data.get("quantity"),
            order_id=body_data.get("order_id"),
            menu_item_id=body_data.get("menu_item_id")
        )
        db.session.add(new_order_item)
        db.session.commit()
        return order_item_schema.dump(new_order_item), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} cannot be null"}, 409

# delete - /order_items/id - DELETE
@order_items_bp.route("/<int:order_item_id>", methods=["DELETE"])
def delete_order_item(order_item_id):
    stmt = db.select(OrderItem).where(OrderItem.id == order_item_id)
    order_item = db.session.scalar(stmt)
    if order_item:
        db.session.delete(order_item)
        db.session.commit()
        return {"message": f"OrderItem with id {order_item_id} deleted"}
    else:
        return {"message": f"OrderItem with id {order_item_id} does not exist"}, 404

# update - /order_items/id - PUT
@order_items_bp.route("/<int:order_item_id>", methods=["PUT"])
def update_order_item(order_item_id):
    stmt = db.select(OrderItem).where(OrderItem.id == order_item_id)
    order_item = db.session.scalar(stmt)
    if order_item:
        body_data = order_item_schema.load(request.get_json())
        order_item.quantity = body_data.get("quantity") or order_item.quantity
        order_item.order_id = body_data.get("order_id") or order_item.order_id
        order_item.menu_item_id = body_data.get("menu_item_id") or order_item.menu_item_id
        db.session.commit()
        return order_item_schema.dump(order_item)
    else:
        return {"message": f"OrderItem with id {order_item_id} does not exist"}, 404