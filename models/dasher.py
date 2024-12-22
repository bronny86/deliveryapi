from init import db, ma

class Dasher(db.Model):
    
    __tablename__ = "dashers"
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    
class DasherSchema(ma.Schema):
    
    ordered = True
    
    class Meta:
        fields = ("id", "name", "phone", "email")
        
dasher_schema = DasherSchema()
dashers_schema = DasherSchema(many=True)