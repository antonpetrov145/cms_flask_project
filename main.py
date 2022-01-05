from db import db
from config import create_app


app = create_app()


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


@app.after_request
def close_request(response):
    try:
        db.session.commit()
    except:
        # if flush is not successful
        db.session.rollback()
    return response


if __name__ == "__main__":
    app.run()
