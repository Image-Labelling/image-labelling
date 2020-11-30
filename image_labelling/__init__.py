from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from flask_bootstrap import Bootstrap
# from sqlalchemy import create_engine
# from .auth import login_manager
# from .database import db

db = SQLAlchemy()
login_manager = LoginManager()

from image_labelling.views import blueprints


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    Bootstrap(app)
    app.config['FLASK_APP'] = 'wsgi.py'
    app.config['WTF_CSRF_SECRET_KEY'] = f'f0182b724eb27ea06c63ca812d9cf5b878974aef53c78fe6'
    app.config['SECRET_KEY'] = f'9e7a1dfc1e156f9a88f63feff2925dd7360db188f2ef9830'
    app.config['DATABASE_CONNECTION_URI'] = f'postgresql+psycopg2://postgres:devmode@localhost:5432/devdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/devdb'
    app.config['UPLOAD_FOLDER'] = './data/'
    app.config['MAX_CONTENT_PATH'] = 100 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {
        'jp2', 'jpf', 'jpx', 'jpm', 'jpe', 'jif', 'jfif', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Application Configuration
    # app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.create_all(app=app)

    # with app.app_context():
    #     from . import routes
    #     from . import auth
    #     from .assets import compile_assets

    #     # Register Blueprints
    #     app.register_blueprint(routes.main_bp)
    #     app.register_blueprint(auth.auth_bp)

    #     # Create Database Models
    #     db.create_all()

    #     # Compile static assets
    #     if app.config['FLASK_ENV'] == 'development':
    #         compile_assets(app)

    #     return app

    return app


# def create_app():
#     """Create app instance"""
#     app = Flask(__name__)


#     db.init_app(app)
#     login_manager.init_app(app)
#     db.create_all(app=app)

#     return app
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
