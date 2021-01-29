from flask import Flask, session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_principal import Principal
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()
migrate = Migrate()
principal = Principal()
session = Session()
csrf = CSRFProtect()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    Bootstrap(app)
    app.config['FLASK_APP'] = 'wsgi.py'
    app.config['WTF_CSRF_SECRET_KEY'] = f'f0182b724eb27ea06c63ca812d9cf5b878974aef53c78fe6'
    app.config['SECRET_KEY'] = f'9e7a1dfc1e156f9a88f63feff2925dd7360db188f2ef9830'
    app.config['DATABASE_CONNECTION_URI'] = f'postgresql+psycopg2://postgres:devmode@localhost:5432/devdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/devdb'
    app.config['UPLOAD_FOLDER'] = './image_labelling/data/'
    app.config['MAX_CONTENT_PATH'] = 100 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {
        'jp2', 'jpf', 'jpx', 'jpm', 'jpe', 'jif', 'jfif', 'png', 'jpg', 'jpeg', 'gif', 'webp'}
    app.config['SESSION_TYPE'] = 'filesystem'

    # Application Configuration
    # app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate.init_app(app, db, render_as_batch=True)
    principal.init_app(app)
    session.init_app(app)
    csrf.init_app(app)

    from image_labelling.views import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.create_all(app=app)

    from .database import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', ssl_context='adhoc')
