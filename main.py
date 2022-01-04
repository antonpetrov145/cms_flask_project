from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

api = Api(app)
migrate = Migrate(compare_type=True)
migrate.init_app(app, db)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.after_request
def close_request(response):
    try:
        db.session.commit()
    except:
        # if flush is not successful
        db.session.rollback()
    return response


[api.add_resource(*route) for route in routes]

if __name__ == "__main__":
    app.run()
