
import os

from routes.expenses import expenses as expenses_blueprint
from flask import Flask, redirect, url_for, render_template
from flask_login import (
    LoginManager,
    login_required,
    current_user
)
from flask_wtf.csrf import CSRFProtect
from routes.dashboard import dashboard as dashboard_blueprint
from config import Config
from models import db, migrate, User
from routes.auth import auth


login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():

    app = Flask(
        __name__,
        instance_relative_config=True
    )

    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Login configuration
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to continue."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(User, int(user_id))

    # Register authentication routes
    app.register_blueprint(auth)
    app.register_blueprint(expenses_blueprint)
    app.register_blueprint(dashboard_blueprint)

    @app.route("/")
    def home():

        if current_user.is_authenticated:
            return redirect(url_for("dashboard.home"))

        return redirect(url_for("auth.login"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
