from flask import request
from flask_restful import Resource
from managers.auth import auth
from managers.posts import PostManager
from models.posts import PostsModel
from schemas.request.posts import PostCreateRequestSchema
from schemas.response.posts import PostCreateResponseSchema
from utils.decorators import permission_required, validate_schema
from utils.helpers import allowed_creators, allowed_updaters


class Posts(Resource):
    def get(self):
        posts = PostsModel.query.all()
        schema = PostCreateResponseSchema()
        return schema.dump(posts, many=True), 200

    @auth.login_required
    @permission_required(allowed_creators)
    @validate_schema(PostCreateRequestSchema)
    def post(self):
        author = auth.current_user()
        PostManager.create(request.get_json(), author.pk)
        return {"message": "Post created!"}, 201


class UpdatePost(Resource):
    @auth.login_required
    @permission_required(allowed_updaters)
    @validate_schema(PostCreateRequestSchema)
    def put(self, pk):
        updated_post = PostManager.update(request.get_json(), pk)
        schema = PostCreateResponseSchema()
        return schema.dump(updated_post)

    @auth.login_required
    @permission_required(allowed_updaters)
    def delete(self, pk):
        PostManager.delete(pk)
        return {"message": "Deleted Post!"}


class AuthorPosts(Resource):
    @auth.login_required
    @permission_required(allowed_creators)
    def get(self, pk):
        posts = PostManager.get_author_posts(pk)
        schema = PostCreateResponseSchema()
        return schema.dump(posts, many=True), 200


class ClientPosts(Resource):
    @auth.login_required
    @permission_required("client")
    def get(self, pk):
        posts = PostManager.get_client_posts(pk)
        schema = PostCreateResponseSchema()
        return schema.dump(posts, many=True), 200
