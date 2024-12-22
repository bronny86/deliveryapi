from init import db, ma

class Customer(db.Model):
    
    __tablename__ = "customers"
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100), nullable=False, unique=True)
    

class CustomerSchema(ma.Schema):
    
    ordered = True
    
    class Meta:
        fields = ("id", "name", "address", "phone")
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)