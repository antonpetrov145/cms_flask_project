# functions for validating schemas and roles
from functools import wraps
from managers.auth import auth
from flask import request
from werkzeug.exceptions import BadRequest, Forbidden


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(f"Invalid fields {errors}")
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def permission_required(permission):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            if not user.role.value in permission:
                raise Forbidden("You don't have access for this request!")
            return f(*args, **kwargs)

        return decorated_function

    return wrapper
