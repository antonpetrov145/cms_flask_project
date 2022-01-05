from managers.auth import AuthManager


def generate_token(user):
    return AuthManager.encode_token(user)
