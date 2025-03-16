from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'views.login'

    from app.models import UserProfile

    @login_manager.user_loader
    def load_user(user_id):
        return UserProfile.query.get(int(user_id))

    from app import views
    views.init_app(app)

    return app