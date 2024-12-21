from marshmallow import fields

from init import db, ma

class Customer(db.Model):
    
    __tablename__ = "custoemrs"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    

class CustomerSchema(ma.Schema):
    
    class Meta:
        fiekds = ("id", "name", "address", "phone")
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)