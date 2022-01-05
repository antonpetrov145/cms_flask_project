import factory
from db import db
from models.enums import UserRolesEnum
from models.posts import PostsModel
from models.users import AuthorUserModel, ClientUserModel


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

    pk = factory.Sequence(lambda n: n + 1)
    username = factory.Faker("first_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role = UserRolesEnum.author


class ClientFactory(BaseFactory):
    class Meta:
        model = ClientUserModel

    pk = factory.Sequence(lambda n: n + 1)
    username = factory.Faker("first_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role = UserRolesEnum.client


class PostFactory(BaseFactory):
    class Meta:
        model = PostsModel

    pk = factory.Sequence(lambda n: n + 1)
    title = factory.Faker("sentence", nb_words=5)
    post_content = factory.Faker("sentence", nb_words=20)
