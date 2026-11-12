from flask import Flask
from config import Config
from app.extensions import db, login_manager, csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in first."

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth import auth
    from app.dashboard import dashboard
    from app.crud import crud

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(crud)

    with app.app_context():
        db.create_all()

    return app
