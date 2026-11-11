import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()
app = create_app(os.getenv("FLASK_CONFIG", "development"))

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))
