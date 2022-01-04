from flask_restful import Resource
from flask import request
from managers.auth import AuthManager, auth
from managers.authors import AuthorManager
from schemas.request.users import (
    RequestLoginAuthorUserSchema,
    RequestRegisterUserSchema,
)
from utils.decorators import permission_required, validate_schema


class RegisterAuthor(Resource):
    @validate_schema(RequestRegisterUserSchema)
    def post(self):
        data = request.get_json()
        token = AuthorManager.register(data)
        return {"token": token}, 201


class LoginAuthor(Resource):
    @validate_schema(RequestLoginAuthorUserSchema)
    def post(self):
        data = request.get_json()
        author = AuthorManager.login(data)
        token = AuthManager.encode_token(author)
        return {"token": token, "role": "author"}, 200


class UpdateAuthor(Resource):
    @auth.login_required
    @permission_required("admin")
    def delete(self, pk):
        AuthorManager.delete(pk)
        return {"message": "Deleted User!"}
