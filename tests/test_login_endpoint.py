from datetime import datetime, timedelta

import jwt
from django.conf import settings


def test_login_with_correct_credentials_and_receive_jwt_token(user, client):
    response = client.post(
        "/login", json={"username": "user", "password": "password"}, auth=False
    )

    assert response.status_code == 200
    assert "token" in response.json()
    decoded = jwt.decode(
        response.json()["token"], settings.JWT_SECRET_KEY, algorithms=["HS256"]
    )
    assert decoded["user"] == "user"
    assert decoded["exp"] > (datetime.now() + timedelta(days=29)).timestamp()


def test_login_with_incorrect_credentials_and_receive_error_message(user, client):
    response = client.post(
        "/login",
        json={"username": "user", "password": "incorrect_password"},
        auth=False,
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Incorrect username or password"}
