from flask import Flask
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from image_labelling.views import blueprints
from .auth import login_manager
from .database import db


def create_app():
    """Create app instance"""
    app = Flask(__name__)
    Bootstrap(app)
    app.config['WTF_CSRF_SECRET_KEY'] = f'f0182b724eb27ea06c63ca812d9cf5b878974aef53c78fe6'
    app.config['SECRET_KEY'] = f'9e7a1dfc1e156f9a88f63feff2925dd7360db188f2ef9830'
    app.config['DATABASE_CONNECTION_URI'] = f'postgresql+psycopg2://postgres:devmode@localhost:5432/devdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/devdb'
    app.config['UPLOAD_FOLDER'] = './data/'
    app.config['MAX_CONTENT_PATH'] = 100 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {
        'jp2', 'jpf', 'jpx', 'jpm', 'jpe', 'jif', 'jfif', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
