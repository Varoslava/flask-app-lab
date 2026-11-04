from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "lab4-secret-key"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

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
@app.errorhandler(413)
def request_entity_too_large(error):
    return "Розмір файлу перевищує максимально допустимі 5 МБ!", 413