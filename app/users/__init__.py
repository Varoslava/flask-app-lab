from flask import Blueprint

from app.extensions import login_manager

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
    template_folder="templates"
)

from app.users.models import User
from app.users import views


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except (TypeError, ValueError):
        return None