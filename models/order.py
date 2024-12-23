from datetime import date

from marshmallow import fields

from init import db, ma

class Order(db.Model):
    __tablename__ = "orders"
    
    id = db.Column(db.Integer, primary_key=True)
    
    order_date = db.Column(db.Date, nullable=False, default=date.today())
    order_total = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    dasher_id = db.Column(db.Integer, db.ForeignKey("dashers.id"))
    
    customer = db.relationship("Customer", back_populates="orders")
    
    dasher = db.relationship("Dasher", back_populates="orders", cascade="all, delete")
    
class OrderSchema(ma.Schema):
    
    ordered = True
    customer = fields.Nested("CustomerSchema", exclude=("orders",))
    dasher = fields.List(fields.Nested("DasherSchema", exclude=("orders",)))
    
    class Meta:
        fields = ("id", "order_date", "order_total", "delivery_address", "customer_id", "dasher_id")
        
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)