from flask import Blueprint, request

from init import db
from models.menu_item import MenuItem, menu_item_schema, menu_items_schema

menu_items_bp = Blueprint("menu_items", __name__, url_prefix="/menu_items")

