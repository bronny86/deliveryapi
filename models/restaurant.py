from marshmallow import fields
from marshmallow.validate import OneOf

from init import db, ma

VALID_CUISINES = ("Italian", "Mexican", "Fast Food", "Chinese", "Indian")

class Restaurant(db.Model):
    __tablename__ = "restaurants"
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    cuisine = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    
class RestaurantSchema(ma.Schema):
    
    cuisine = fields.String(validate=OneOf(VALID_CUISINES))
    
    ordered = True
    
    class Meta:
        fields = ("id", "name", "address", "cuisine", "phone")
        
restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)