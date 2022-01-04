from db import db
from models.posts import PostsModel
from werkzeug.exceptions import NotFound
from managers.auth import auth


class PostManager:
    @staticmethod
    def create(post_data, author):
        post_data["author_pk"] = author
        post = PostsModel(**post_data)
        db.session.add(post)
        db.session.flush()
        return post

    @staticmethod
    def update(post_data, pk):
        post_pk = PostsModel.query.filter_by(pk=pk)
        post = post_pk.first()
        if not post:
            raise NotFound("Post not found")
        user = auth.current_user()

        if user.role == "author":
            if not user.pk == post.author_pk:
                raise NotFound("Post not found")

        post_pk.update(post_data)
        db.session.add(post)
        db.session.flush()
        return post

    @staticmethod
    def delete(pk):
        post_pk = PostsModel.query.filter_by(pk=pk)
        post = post_pk.first()
        if not post:
            raise NotFound("Post not found")

        db.session.delete(post)
        db.session.flush()

    @staticmethod
    def get_author_posts(author_pk):
        posts = PostsModel.query.filter_by(author_pk=author_pk)
        if not posts:
            return {"message": "User has no posts!"}
        return posts.all()

    @staticmethod
    def get_client_posts(client_pk):
        posts = PostsModel.query.filter_by(client_pk=client_pk)
        if not posts:
            return {"message": "User has no posts!"}
        return posts.all()
