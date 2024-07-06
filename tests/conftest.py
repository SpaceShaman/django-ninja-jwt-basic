from datetime import datetime, timedelta
from typing import Dict

import jwt
import pytest
from django.conf import settings
from django.contrib.auth.models import User
from ninja.testing import TestClient
from ninja.testing.client import NinjaResponse

from django_ninja_jwt_basic.api import router


class TestClientAuth(TestClient):
    def request(
        self,
        method: str,
        path: str,
        data: Dict | None = None,
        json=None,
        auth: bool = True,
        user: str = "user",
        **request_params,
    ) -> NinjaResponse:
        if auth:
            token = jwt.encode(
                {"user": user, "exp": datetime.now() + timedelta(days=30)},
                settings.JWT_SECRET_KEY,
            )
            request_params["headers"] = {"Authorization": f"Bearer {token}"}

        return super().request(method, path, data, json, **request_params)


@pytest.fixture(scope="session")
def client() -> TestClientAuth:
    return TestClientAuth(router)


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(username="user", password="password")
