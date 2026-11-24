from flask import Blueprint

posts_bp = Blueprint(
    "posts",
    __name__,
    url_prefix="/post",
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)

from app.posts.models import Post
from app.users.models import User
from app.posts import views