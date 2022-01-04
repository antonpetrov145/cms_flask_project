from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from models.users import (
    AdminUserModel,
    AuthorUserModel,
    ClientUserModel,
    EditorUserModel,
)
from werkzeug.exceptions import BadRequest, Unauthorized


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.pk,
            "exp": datetime.utcnow() + timedelta(days=2),
            "type": user.__class__.__name__,
        }
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            data = jwt.decode(token, key=config("SECRET_KEY"), algorithms=["HS256"])
            return data["sub"], data["type"]
        except jwt.ExpiredSignatureError:
            raise BadRequest("Token Expired!")
        except jwt.InvalidTokenError:
            raise BadRequest("Invalid Token!")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        user_pk, type_user = AuthManager.decode_token(token)
        return eval(f"{type_user}.query.filter_by(pk={user_pk}).first()")
    except:
        raise Unauthorized("Token is missing or invalid!")
