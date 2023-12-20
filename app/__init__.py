from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os


def create_app():
    app = Flask(__name__)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Logging setup
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/myapp.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('MyApp startup')

    return app
