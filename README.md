# django-ninja-jwt-basic

![GitHub License](https://img.shields.io/github/license/SpaceShaman/django-ninja-jwt-basic)
![Tests](https://img.shields.io/github/actions/workflow/status/SpaceShaman/django-ninja-jwt-basic/release.yml?label=tests)
[![Codecov](https://img.shields.io/codecov/c/github/SpaceShaman/django-ninja-jwt-basic)](https://codecov.io/gh/SpaceShaman/django-ninja-jwt-basic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-ninja-jwt-basic)](https://pypi.org/project/django-ninja-jwt-basic)
[![PyPI - Version](https://img.shields.io/pypi/v/django-ninja-jwt-basic)](https://pypi.org/project/django-ninja-jwt-basic)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Simple JWT based authentication designed for Django and Django Ninja. This package aims to provide a minimalistic approach to JWT authentication with the least amount of dependencies, making it easy to integrate and use in your projects.

## Installation

```bash
pip install django-ninja-jwt-basic
```

## Configuration

1. Add the following settings to your Django settings:

    ```python
    JWT_SECRET_KEY = 'your_secret key' # Required
    ```

2. Add the app to your `INSTALLED_APPS` in your Django settings:

    ```python
    INSTALLED_APPS = [
        ...
        'django_ninja_jwt_basic',
        ...
    ]
    ```

## Usage

Next, add router to your Django Ninja API and protect your endpoints

```python
from ninja import NinjaAPI
from django_ninja_jwt_basic import JWTAuth

api = NinjaAPI(auth=JWTAuth())
api.add_router('/auth', 'django_ninja_jwt_basic.router')
```

If you don't want protect all endpoints, you can use `JWTAuth` class directly in your endpoints or routers like below:

```python
from ninja import Router
from django_ninja_jwt_basic import JWTAuth

router = Router(auth=JWTAuth())

@router.get('/protected')
def protected(request):
    return {'message': 'This is a protected endpoint'}
```

``` python
from django_ninja_jwt_basic import JWTAuth

@api.get('/protected', auth=JWTAuth())
def protected(request):
    return {'message': 'This is a protected endpoint'}
```

You can find more information about protecting endpoints in the [Django Ninja documentation](https://django-ninja.dev/guides/authentication/)
