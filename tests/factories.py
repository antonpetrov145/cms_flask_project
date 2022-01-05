import factory
from db import db
from models.enums import UserRolesEnum
from models.users import AuthorUserModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class AuthorFactory(BaseFactory):
    class Meta:
        model = AuthorUserModel

    pk = factory.Sequence(lambda n: n)
    username = factory.Faker("username")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role = UserRolesEnum.author
