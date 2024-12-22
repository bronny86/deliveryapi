import os

from flask import Flask

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.customer_controller import customers_bp



def create_app():
    app = Flask(__name__)
    
    print("Server started")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://delivery_dev:123456@localhost:5432/delivery_db"
    
    db.init_app(app)
    ma.init_app(app)
    
    app.register_blueprint(db_commands)
    app.register_blueprint(customers_bp)
    
    return app