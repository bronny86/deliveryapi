from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.dasher import Dasher, dasher_schema, dashers_schema

dashers_bp = Blueprint("dashers", __name__, url_prefix="/dashers")

# read all - /dashers GET
@dashers_bp.route("/")
def get_dashers():
    stmt = db.select(Dasher)
    dashers_list = db.session.scalars(stmt)
    data = dashers_schema.dump(dashers_list)
    return data

# read one - /dashers/id - GET
@dashers_bp.route("/<int:dasher_id>")
def get_dasher(dasher_id):
    stmt = db.select(Dasher).filter_by(id=dasher_id)
    dasher = db.session.scalar(stmt)
    if dasher:
        data = dasher_schema.dump(dasher)
        return data
    else:
        return {"message": f"Dasher with id {dasher_id} does not exist"}, 404

# create - /dashers - POST
@dashers_bp.route("/", methods=["POST"])
def create_dasher():
    try:
        body_data = dasher_schema.load(request.get_json())
        new_dasher = Dasher(
            name=body_data.get("name"),
            phone=body_data.get("phone"),
            email=body_data.get("email")
        )
        db.session.add(new_dasher)
        db.session.commit()
        return dasher_schema.dump(new_dasher), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field {err.orig.diag.column_name} cannot be null"}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Email already in use"}, 409

# delete - /dashers/id - DELETE
@dashers_bp.route("/<int:dasher_id>", methods=["DELETE"])
def delete_dasher(dasher_id):
    stmt = db.select(Dasher).where(Dasher.id == dasher_id)
    dasher = db.session.scalar(stmt)
    if dasher:
        db.session.delete(dasher)
        db.session.commit()
        return {"message": f"Dasher with id {dasher_id} deleted"}
    else:
        return {"message": f"Dasher with id {dasher_id} does not exist"}, 404

# update - /dashers/id - PUT
@dashers_bp.route("/<int:dasher_id>", methods=["PUT", "PATCH"])
def update_dasher(dasher_id):
    stmt = db.select(Dasher).where(Dasher.id == dasher_id)
    dasher = db.session.scalar(stmt)
    if dasher:
        body_data = dasher_schema.load(request.get_json())
        dasher.name = body_data.get("name") or dasher.name
        dasher.phone = body_data.get("phone") or dasher.phone
        dasher.email = body_data.get("email") or dasher.email
        db.session.commit()
        return dasher_schema.dump(dasher)
    else:
        return {"message": f"Dasher with id {dasher_id} does not exist"}, 404