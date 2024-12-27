import os

from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.customer_controller import customers_bp
from controllers.dasher_controller import dashers_bp
from controllers.restaurant_controller import restaurants_bp
from controllers.order_controller import orders_bp
from controllers.menu_item_controller import menu_items_bp
from controllers.order_item_controller import order_items_bp


def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    
    app.json.sort_keys = False
    
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
    app.register_blueprint(orders_bp)
    app.register_blueprint(menu_items_bp)
    app.register_blueprint(order_items_bp)
    
    return app