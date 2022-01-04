from flask_restful import Resource
from flask import request
from managers.auth import AuthManager, auth
from managers.clients import ClientManager
from schemas.request.users import (
    RequestLoginClientUserSchema,
    RequestRegisterClientUserSchema,
)
from utils.decorators import permission_required, validate_schema


class RegisterClient(Resource):
    @validate_schema(RequestRegisterClientUserSchema)
    def post(self):
        data = request.get_json()
        token = ClientManager.register(data)
        return {"token": token}, 201


class LoginClient(Resource):
    @validate_schema(RequestLoginClientUserSchema)
    def post(self):
        data = request.get_json()
        author = ClientManager.login(data)
        token = AuthManager.encode_token(author)
        return {"token": token, "role": "client"}, 200


class UpdateClient(Resource):
    @auth.login_required
    @permission_required("admin")
    def delete(self, pk):
        ClientManager.delete(pk)
        return {"message": "Deleted User!"}
