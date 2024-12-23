import os

from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.customer_controller import customers_bp
from controllers.dasher_controller import dashers_bp
from controllers.restaurant_controller import restaurants_bp


def create_app():
    app = Flask(__name__)
    
    print("Server started")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://delivery_dev:123456@localhost:5432/delivery_db"
    
    db.init_app(app)
    ma.init_app(app)
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"message": err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {"message": str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"message": str(err)}, 404
    
    app.register_blueprint(db_commands)
    app.register_blueprint(customers_bp)
    app.register_blueprint(dashers_bp)
    app.register_blueprint(restaurants_bp)
    
    return app