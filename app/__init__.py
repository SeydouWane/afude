from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel
from .models import db, User
from .routes.public import public_bp
app.register_blueprint(public_bp)

login_manager = LoginManager()
babel = Babel()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    # Initialisation des extensions
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    migrate = Migrate(app, db)

    # Gestion des sessions
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Enregistrement des Blueprints
    from .routes.public import public_bp
    from .routes.admin import admin_bp
    from .routes.tourist import tourist_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(tourist_bp, url_prefix='/tourist')

    return app
