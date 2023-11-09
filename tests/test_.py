import time

import pytest

from tests.models import client, jwt_validity_time


def test_get_salary():
    response = client.post(
        "/login", json={"username": "user1", "password": "password1"}
    )
    token = response.json()["access_token"]
    response = client.get("/users/salary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"salary": 1000, "salary_increase_date": "2023-12-12"}


@pytest.mark.parametrize(
    ["username", "password"], 
    [
        pytest.param("user1", "password2", id="incorrect password"),
        pytest.param("user3", "password2", id="non-existing user"),
        pytest.param("user1", "         ", id="empty field"),
        pytest.param("user1", "!@#$%^&*()_+-=[]{|;:',.<>/?`~}", id="special signs"),
        pytest.param("user1", True, id="Bool password's type"),
        pytest.param("user1", 1111, id="int type"),
        pytest.param("user1", 1.11, id="float type"),
    ]
)
def test_login_invalid_credentials(username, password):
    response = client.post("/login", json={"username": username, "password": password})
    assert response.status_code == 401
    assert response.text == ""


@pytest.mark.parametrize(
    ["username", "password"], 
    [
        pytest.param("user1", None, id="None type"),
        pytest.param("user1", ["password1"], id="list type"),
        pytest.param("user1", {"user1": "password1"}, id="dict type"),
    ]
)
def test_login_invalid_passw_types(username, password):
    response = client.post("/login", json={"username": username, "password": password})
    assert response.status_code == 422


def test_get_salary_invalid_token():
    response = client.get(
        "/users/salary", headers={"Authorization": f"Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.text == ""


def test_get_salary_expired_token():
    token = client.post(
        "/login", json={"username": "user1", "password": "password1"}
    ).json()["access_token"]
    time.sleep(jwt_validity_time.total_seconds() + 1)
    response = client.get("/users/salary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {"message": "Token expired"}
