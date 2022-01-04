from decouple import config


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_ADDRESS')}:{config('DB_PORT')}/{config('DB_NAME')}"
