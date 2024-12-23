from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.order import Order, order_schema, orders_schema

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

# read all - /orders GET
@orders_bp.route("/")
def get_orders():
    stmt = db.select(Order)
    orders_list = db.session.scalars(stmt)
    data = orders_schema.dump(orders_list)
    return data

# read one - /orders/id - GET
@orders_bp.route("/<int:order_id>")
def get_order(order_id):
    stmt = db.select(Order).filter_by(id=order_id)
    order = db.session.scalar(stmt)
    if order:
        data = order_schema.dump(order)
        return data
    else:
        return {"message": f"Order with id {order_id} does not exist"}, 404

# create - /orders - POST
@orders_bp.route("/", methods=["POST"])
def create_order():
    try:
        body_data = order_schema.load(request.get_json())
        new_order = Order(
            order_date=body_data.get("order_date"),
            order_total=body_data.get("order_total"),
            delivery_address=body_data.get("delivery_address"),
            customer_id=body_data.get("customer_id"),
            dasher_id=body_data.get("dasher_id")
        )
        db.session.add(new_order)
        db.session.commit()
        return order_schema.dump(new_order), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} cannot be null"}, 409

# delete - /orders/id - DELETE
@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    stmt = db.select(Order).where(Order.id == order_id)
    order = db.session.scalar(stmt)
    if order:
        db.session.delete(order)
        db.session.commit()
        return {"message": f"Order with id {order_id} deleted"}
    else:
        return {"message": f"Order with id {order_id} does not exist"}, 404

# update - /orders/id - PUT
@orders_bp.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    stmt = db.select(Order).where(Order.id == order_id)
    order = db.session.scalar(stmt)
    if order:
        try:
            body_data = order_schema.load(request.get_json())
            order.order_date = body_data.get("order_date") or order.order_date
            order.order_total = body_data.get("order_total") or order.order_total
            order.delivery_address = body_data.get("delivery_address") or order.delivery_address
            order.customer_id = body_data.get("customer_id") or order.customer_id
            order.dasher_id = body_data.get("dasher_id") or order.dasher_id
            db.session.commit()
            return order_schema.dump(order)
        except IntegrityError as err:
            if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {"message": f"The field {err.orig.diag.column_name} cannot be null"}, 409
    else:
        return {"message": f"Order with id {order_id} does not exist"}, 404