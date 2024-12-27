from marshmallow import fields
from init import db, ma

class OrderItem(db.Model):
    __tablename__ = "order_items"
    
    id = db.Column(db.Integer, primary_key=True)
    
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"))
    
    quantity = db.Column(db.Integer, nullable=False)
    
    order = db.relationship("Order", back_populates="order_items")
    menu_item = db.relationship("MenuItem", back_populates="order_items")
    
class OrderItemSchema(ma.Schema):
    
    ordered = True
    order = fields.Nested("OrderSchema", exclude=["order_items"])
    menu_item = fields.Nested("MenuItemSchema", exclude=["order_items"])
    
    class Meta:
        fields = ("id", "order_id", "menu_item_id", "quantity", "order", "menu_item")
        
order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)