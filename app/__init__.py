from pathlib import Path
from flask import Flask, render_template
from app.config import config_by_name
from app.extensions import db, migrate


def create_app(config_name="development"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    app.config["SQLALCHEMY_ECHO"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app import views
    from app.users import users_bp
    from app.products import products_bp
    from app.posts import posts_bp

    app.register_blueprint(views.main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(posts_bp)

    @app.context_processor
    def inject_portfolio():
        return {"person": views.portfolio}

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html", title="Сторінку не знайдено"), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return "Розмір файлу перевищує максимально допустимі 5 МБ!", 413

    return app