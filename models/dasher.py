from marshmallow import fields

from init import db, ma

class Dasher(db.Model):
    
    __tablename__ = "dashers"
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    
    orders = db.relationship("Order", back_populates="dasher", cascade="all, delete")
    
class DasherSchema(ma.Schema):
    
    
    orders = fields.List(fields.Nested("OrderSchema", exclude=["dasher"]))
    
    class Meta:
        fields = ("id", "name", "phone", "email", "orders")
        
dasher_schema = DasherSchema()
dashers_schema = DasherSchema(many=True)