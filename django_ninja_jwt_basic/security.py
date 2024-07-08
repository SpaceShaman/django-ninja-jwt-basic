import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from ninja.errors import HttpError
from ninja.security import HttpBearer


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            decoded = jwt.decode(
                token, getattr(settings, "JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            get_user_model().objects.get(username=decoded["user"])
            return decoded["user"]
        except jwt.PyJWTError:
            return None
        except ObjectDoesNotExist as e:
            raise HttpError(403, "User does not exist") from e
