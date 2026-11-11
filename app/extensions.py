from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Розширення створюються окремо від Flask-застосунку.
db = SQLAlchemy()
migrate = Migrate()
