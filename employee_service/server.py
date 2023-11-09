from datetime import timedelta

import jwt
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer

from employee_service.auth import (
    Credentials,
    InvalidCredentialsException,
    JwtToken,
    authenticate_user,
    gen_password_hash,
)
from employee_service.models import Employee, SalaryResponse
from employee_service.storage import Storage, UserNotFound


def make_app(
    storage: Storage,
    jwt_hs256_secret_key,
    jwt_validity_time: timedelta = timedelta(days=1),
) -> FastAPI:
    """Create FastAPI application."""

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    app = FastAPI()

    async def get_user(token: str = Depends(oauth2_scheme)) -> Employee:
        username = JwtToken.decode_username(token, jwt_hs256_secret_key)
        return await storage.get_user(username)

    @app.post("/login")
    async def login(user: Credentials) -> JwtToken:
        try:
            await authenticate_user(user, storage)
        except UserNotFound:
            # don't leak information about whether the user exists or not.
            raise InvalidCredentialsException()

        return JwtToken.generate(user.username, jwt_validity_time, jwt_hs256_secret_key)

    @app.get("/users/salary")
    async def get_salary(user: Employee = Depends(get_user)) -> SalaryResponse:
        return SalaryResponse(
            salary=user.salary, salary_increase_date=user.salary_increase_date
        )

    _attach_exception_handlers(app)
    return app


def _attach_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserNotFound)
    async def on_user_not_found(request, exc):
        return JSONResponse(status_code=404, content={"message": "User not found"})

    @app.exception_handler(InvalidCredentialsException)
    async def on_invalid_credentials(request, exc):
        # don't give any additional information for security reasons.
        return Response(status_code=401)

    @app.exception_handler(jwt.ExpiredSignatureError)
    async def on_token_expired(request, exc):
        return JSONResponse(status_code=401, content={"message": "Token expired"})

    @app.exception_handler(jwt.InvalidTokenError)
    async def on_invalid_token(request, exc):
        # don't give any additional information for security reasons.
        return Response(status_code=401)
