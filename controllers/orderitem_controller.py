from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.orderitem import OrderItem, order_item_schema, order_items_schema

order_items_bp = Blueprint("order_items", __name__, url_prefix="/order_items")

# read all - /order_items GET
@order_items_bp.route("/")
def get_order_items():
    order_item_id = request.args.get("order_item_id")
    if order_item_id:
        stmt = db.select(OrderItem).filter_by(order_item_id=order_item_id)
    else:
        stmt = db.select(OrderItem)
    order_items_list = db.session.scalars(stmt)
    return order_items_schema.dump(order_items_list)

# read one - /order_items/id - GET
@order_items_bp.route("/<int:order_item_id>")
def get_order_item(order_item_id):
    stmt = db.select(OrderItem).filter_by(id=order_item_id)
    order_item = db.session.scalar(stmt)
    if order_item:
        data = order_item_schema.dump(order_item)
        return data
    else:
        return {"message": f"Order item with id {order_item_id} does not exist"}, 404

# create - /order_items - POST
# delete - /order_items/id - DELETE
# update - /order_items/id - PUT

