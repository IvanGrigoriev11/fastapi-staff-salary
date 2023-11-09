import datetime

from datetime import date
from fastapi.testclient import TestClient

from employee_service.auth import gen_password_hash
from employee_service.models import Employee
from employee_service.storage import InMemoryStorage
from employee_service.server import make_app


storage = InMemoryStorage(
    users=[
        Employee(
            username="user1",
            salary=1000,
            salary_increase_date=date.fromisoformat("2023-12-12"),
        ),
        Employee(
            username="user2",
            salary=2000,
            salary_increase_date=date.fromisoformat("2024-10-10"),
        ),
    ],
    password_hashes={
        "user1": gen_password_hash("password1"),
        "user2": gen_password_hash("password2"),
    },
)
jwt_secret = "test_jwt_hs256_secret_key"
jwt_validity_time = datetime.timedelta(seconds=3)

client = TestClient(make_app(storage, jwt_secret, jwt_validity_time))

