import os
from datetime import date

import typer
import uvicorn

from employee_service.auth import gen_password_hash
from employee_service.models import Employee
from employee_service.server import make_app
from employee_service.storage import InMemoryStorage


def main(is_testing: bool = False):
    """
    Launches the uvicorn server and provides two implementations depending on --is-testing flag.

    If --is-testing flag is set to True, it provides an implementation based on InMemory storage.
    If --is-testing is False, it provides an implementation based on production storage
    (e.g. PostgreSQL, MySQL, etc). This implementation has not yet been implemented.
    """

    if is_testing:
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
    else:
        assert False, "Not implemented yet. Needs production storage."

    jwt_hs256_secret_key = os.environ["JWT_SECRET_KEY"]
    uvicorn.run(make_app(storage, jwt_hs256_secret_key), host="0.0.0.0", port=8000)


if __name__ == "__main__":
    typer.run(main)
