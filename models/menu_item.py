from marshmallow import fields

from init import db, ma

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    
    restaurant = db.relationship("Restaurant", back_populates="menu_items")
    
class MenuItemSchema(ma.Schema):
    
    ordered = True
    
    restaurant = fields.Nested("RestaurantSchema", exclude=("menu_items",))
    
    class Meta:
        fields = ("id", "name", "price", "restaurant_id")
        
menu_item_schema = MenuItemSchema()
menu_items_schema = MenuItemSchema(many=True)