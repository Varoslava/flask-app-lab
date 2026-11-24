from flask import Blueprint

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
    template_folder="templates"
)

from app.users.models import User
from app.users import views