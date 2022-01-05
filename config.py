from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from db import db
from resources.routes import routes


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_ADDRESS')}:{config('DB_PORT')}/{config('DB_NAME')}"


class TestingConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_ADDRESS')}:{config('DB_PORT')}/{config('TESTING_DB_NAME')}"


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    api = Api(app)
    migrate = Migrate(compare_type=True)
    migrate.init_app(app, db)
    db.init_app(app)

    [api.add_resource(*route) for route in routes]
    return app
