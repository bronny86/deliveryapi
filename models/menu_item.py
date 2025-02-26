from marshmallow import fields

from init import db, ma

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    
    restaurant = db.relationship("Restaurant", back_populates="menu_items")
    
    order_items = db.relationship("OrderItem", back_populates="menu_item", cascade="all, delete")
    
class MenuItemSchema(ma.Schema):
    
    ordered = True
    
    restaurant = fields.Nested("RestaurantSchema", only=["name"])
    
    order_items = fields.List(fields.Nested("OrderItemSchema", only=["quantity"]))
    
    class Meta:
        fields = ("id", "name", "price", "restaurant_id", "restaurant", "order_items")
        
menu_item_schema = MenuItemSchema()
menu_items_schema = MenuItemSchema(many=True)