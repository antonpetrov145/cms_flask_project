from flask_restful import Resource
from flask import request
from managers.auth import AuthManager
from managers.admins import AdminManager
from schemas.request.users import (
    RequestLoginAdminUserSchema,
    RequestRegisterUserSchema,
)
from utils.decorators import validate_schema, permission_required


class RegisterAdmin(Resource):
    @validate_schema(RequestRegisterUserSchema)
    @permission_required("admin")
    def post(self):
        data = request.get_json()
        token = AdminManager.register(data)
        return {"token": token}, 201


class LoginAdmin(Resource):
    @validate_schema(RequestLoginAdminUserSchema)
    def post(self):
        data = request.get_json()
        admin = AdminManager.login(data)
        token = AuthManager.encode_token(admin)
        return {"token": token, "role": "admin"}, 200
