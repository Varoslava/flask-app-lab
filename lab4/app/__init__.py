from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "lab4-secret-key"

from app import views


@app.context_processor
def inject_portfolio():
    return {
        "person": views.portfolio
    }


from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)