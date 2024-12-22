from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.customer import Customer, customer_schema, customers_schema

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# read all - /customers GET
@customers_bp.route("/")
def get_customers():
    stmt = db.select(Customer)
    customers_list = db.session.scalars(stmt)
    data = customers_schema.dump(customers_list)
    return data

# read one - /customers/id - GET
@customers_bp.route("/<int:customer_id>")
def get_customer(customer_id):
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    if customer:
        data = customer_schema.dump(customer)
        return data
    else:
        return {"message": f"Customer with id {customer_id} does not exist"}, 404

# create - /customers - POST
@customers_bp.route("/", methods=["POST"])
def create_customer():
    try:
        body_data = customer_schema.load(request.get_json())
        new_customer = Customer(
            name=body_data.get("name"),
            address=body_data.get("address"),
            phone=body_data.get("phone")
        )
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.dump(new_customer), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} cannot be null"}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Phone number already in use"}, 409

# delete - /customers/id - DELETE
@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    stmt = db.select(Customer).where(Customer.id == customer_id)
    customer = db.session.scalar(stmt)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return {"message": f"Customer with id {customer_id} deleted"}
    else:
        return {"message": f"Customer with id {customer_id} does not exist"}, 404

# update - /customers/id - PUT
@customers_bp.route("/<int:customer_id>", methods=["PUT", "PATCH"])
def update_customer(customer_id):
    stmt = db.select(Customer).filter_by(id = customer_id)
    customer = db.session.scalar(stmt)
    body_data = customer_schema.load(request.get_json(), partial=True)
    if customer:
        customer.name = body_data.get("name") or customer.name
        customer.address = body_data.get("address") or customer.address
        customer.phone = body_data.get("phone") or customer.phone
        db.session.commit()
        return customer_schema.dump(customer)
    else:
        return {"message": f"Customer with id {customer_id} does not exist"}, 404