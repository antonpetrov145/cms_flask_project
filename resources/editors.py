from flask_restful import Resource
from flask import request
from managers.auth import AuthManager, auth
from managers.editors import EditorManager
from schemas.request.users import (
    RequestLoginEditorUserSchema,
    RequestRegisterUserSchema,
)
from utils.decorators import permission_required, validate_schema


class RegisterEditor(Resource):
    @validate_schema(RequestRegisterUserSchema)
    def post(self):
        data = request.get_json()
        token = EditorManager.register(data)
        return {"token": token}, 201


class LoginEditor(Resource):
    @validate_schema(RequestLoginEditorUserSchema)
    def post(self):
        data = request.get_json()
        author = EditorManager.login(data)
        token = AuthManager.encode_token(author)
        return {"token": token, "role": "editor"}, 200


class UpdateEditor(Resource):
    @auth.login_required
    @permission_required("admin")
    def delete(self, pk):
        EditorManager.delete(pk)
        return {"message": "Deleted User!"}, 204
