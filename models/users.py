from db import db

from models.enums import UserRolesEnum


class BaseUserModel(db.Model):
    __abstract__ = True

    pk = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


class AdminUserModel(BaseUserModel):
    __tablename__ = "administrators"

    role = db.Column(
        db.Enum(UserRolesEnum), default=UserRolesEnum.admin, nullable=False
    )


class AuthorUserModel(BaseUserModel):
    __tablename__ = "authors"

    posts = db.relationship("PostsModel", backref="author", lazy="dynamic")
    role = db.Column(
        db.Enum(UserRolesEnum), default=UserRolesEnum.author, nullable=False
    )


class ClientUserModel(BaseUserModel):
    __tablename__ = "clients"

    posts = db.relationship("PostsModel", backref="client", lazy="dynamic")
    iban = db.Column(db.String(22))
    role = db.Column(
        db.Enum(UserRolesEnum), default=UserRolesEnum.client, nullable=False
    )


class EditorUserModel(BaseUserModel):
    __tablename__ = "editors"

    role = db.Column(
        db.Enum(UserRolesEnum), default=UserRolesEnum.editor, nullable=False
    )
