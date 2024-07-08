from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from ninja import Router, Schema
from ninja.errors import HttpError

router = Router(tags=["auth"])


class CredentialsSchema(Schema):
    username: str
    password: str


class TokenSchema(Schema):
    token: str


@router.post("/login", response=TokenSchema, auth=None)
def login(request, data: CredentialsSchema) -> dict[str, str]:
    if user := authenticate(username=data.username, password=data.password):
        return {
            "token": jwt.encode(
                {
                    "user": user.get_username(),
                    "exp": datetime.now() + timedelta(days=30),
                },
                getattr(settings, "JWT_SECRET_KEY"),
            )
        }
    raise HttpError(403, "Incorrect username or password")
