from db import db
from datetime import datetime


class PostsModel(db.Model):
    __tablename__ = "posts"

    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    post_content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    author_pk = db.Column(db.Integer, db.ForeignKey("authors.pk"))
    client_pk = db.Column(db.Integer, db.ForeignKey("clients.pk"))
