from typing import Protocol

from employee_service.models import Employee


class StorageException(Exception):
    """Base exception for storage errors."""


class UserNotFound(StorageException):
    ...


class Storage(Protocol):
    """Storage interface for accessing user data."""

    async def get_user(self, username: str) -> Employee:
        ...

    async def get_password_hash(self, username: str) -> bytes:
        ...


class InMemoryStorage(Storage):
    """Storage interface for working with data from in-memory."""

    def __init__(
        self, users: list[Employee], password_hashes: dict[str, bytes]
    ) -> None:
        self._users = {user.username: user for user in users}
        self._password_hashes = password_hashes

    async def get_user(self, username: str) -> Employee:
        if username in self._users:
            return self._users[username]

        raise UserNotFound()

    async def get_password_hash(self, username: str) -> bytes:
        if username in self._password_hashes:
            return self._password_hashes[username]

        raise UserNotFound()
