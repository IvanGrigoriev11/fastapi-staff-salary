from dataclasses import dataclass
from datetime import datetime, timedelta

import bcrypt
import jwt

from employee_service.storage import Storage


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


class InvalidCredentialsException(Exception):
    ...


def gen_password_hash(password: str) -> bytes:
    """Generate password hash. The hash includes the algorithm info and salt used."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


async def authenticate_user(credentials: Credentials, storage: Storage) -> None:
    """Check if user exists and password is correct."""

    hashed_password = await storage.get_password_hash(credentials.username)
    if not bcrypt.checkpw(credentials.password.encode(), hashed_password):
        raise InvalidCredentialsException()


@dataclass(frozen=True)
class JwtToken:
    access_token: str
    token_type: str

    @staticmethod
    def generate(username: str, expiration_time: timedelta, hs256_secret: str):
        """Generate JWT token with expiration time."""
        token: str = jwt.encode(
            {"sub": username, "exp": datetime.utcnow() + expiration_time},
            hs256_secret,
            algorithm="HS256",
        )
        return JwtToken(
            access_token=token,
            token_type="bearer",
        )

    @staticmethod
    def decode_username(token: str, hs256_secret: str) -> str:
        """Decode username from JWT token."""
        return jwt.decode(token, hs256_secret, algorithms="HS256")["sub"]
