import factory
from db import db
from models.enums import UserRolesEnum
from models.users import AuthorUserModel
from models.posts import PostsModel
from random import randint


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        author = super().create(**kwargs)
        db.session.add(author)
        db.session.flush()
        return author


class AuthorFactory(BaseFactory):
    class Meta:
        model = AuthorUserModel

    pk = factory.Sequence(lambda n: n + 1)
    username = factory.Faker("first_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role = UserRolesEnum.author


class PostFactory(BaseFactory):
    class Meta:
        model = PostsModel

    pk = factory.Sequence(lambda n: n)
    title = factory.Faker("first_name")
    post_content = factory.Faker("email")
    author_pk = str(randint(1, 9))
