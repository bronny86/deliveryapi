import os

from flask import Flask

from init import db, ma


def create_app():
    app = Flask(__name__)
    
    print("Server started")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://delivery_dev:123456@localhost:5432/delivery_db"
    
    db.init_app(app)
    ma.init_app(app)
    
    return app