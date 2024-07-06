# test_check_correct_token_with_no_user_in_db_and_receive_403_response
# test_check_correct_token_with_user_in_db_withouth_permission_and_receive_403_response
from datetime import datetime, timedelta

import jwt
from django.conf import settings

from django_ninja_jwt_basic.api import router
from django_ninja_jwt_basic.security import JWTAuth


@router.get("/me", auth=JWTAuth())
def me(request) -> dict[str, str]:
    return {"user": request.auth}


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


def test_check_correct_token_and_receive_200_response(user, client):
    exp = datetime.now() + timedelta(days=30)
    token = jwt.encode(
        {"user": "user", "exp": exp},
        settings.JWT_SECRET_KEY,
    )

    response = client.get(
        "/me", headers={"Authorization": f"Bearer {token}"}, auth=False
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["user"] == "user"


def test_check_incorrect_token_and_receive_401_response(user, client):
    response = client.get(
        "/me", headers={"Authorization": "Bearer incorrect_token"}, auth=False
    )
    assert response.status_code == 401


def test_check_no_token_and_receive_401_response(user, client):
    response = client.get("/me", auth=False)
    assert response.status_code == 401


def test_check_expired_token_and_receive_401_response(user, client):
    exp = datetime.now() - timedelta(days=1)
    token = jwt.encode(
        {"user": "user", "exp": exp},
        settings.JWT_SECRET_KEY,
    )

    response = client.get(
        "/me", headers={"Authorization": f"Bearer {token}"}, auth=False
    )
    assert response.status_code == 401
