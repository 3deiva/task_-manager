from flask import Flask
from database.db import init_db
from api.routes import api_bp
from auth.auth import auth_bp
from user.user import user_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["DATABASE"] = "app.db"

init_db(app)

app.register_blueprint(api_bp,  url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")

if __name__ == "__main__":
    app.run(debug=True)
