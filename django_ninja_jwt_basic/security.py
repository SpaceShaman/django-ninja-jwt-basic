import jwt
from django.conf import settings
from ninja.security import HttpBearer


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            decoded = jwt.decode(
                token, getattr(settings, "JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            return decoded["user"]
        except jwt.PyJWTError:
            return None
