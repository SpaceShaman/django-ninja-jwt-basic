from datetime import datetime, timedelta

import jwt
from django.conf import settings

from django_ninja_jwt_basic.api import router
from django_ninja_jwt_basic.security import JWTAuth


@router.get("/me", auth=JWTAuth())
def me(request) -> dict[str, str]:
    return {"user": request.auth}


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


def test_check_correct_token_with_no_user_in_db_and_receive_403_response(user, client):
    exp = datetime.now() + timedelta(days=30)
    token = jwt.encode(
        {"user": "non_existing_user", "exp": exp},
        settings.JWT_SECRET_KEY,
    )

    response = client.get(
        "/me", headers={"Authorization": f"Bearer {token}"}, auth=False
    )
    assert response.status_code == 403
