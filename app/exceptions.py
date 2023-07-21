from typing import Any, Optional, Dict

from fastapi import HTTPException
from starlette import status


class UserDoesNotExistException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Bad request"
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidUsernameOrPasswordException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Incorrect username or password"
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class InvalidTokenException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not validate credentials"
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)
