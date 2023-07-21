from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
from starlette.exceptions import HTTPException

from app import schemas, crud
from app.exceptions import InvalidTokenException
from app.schemas import TokenData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        try:
            auth = conn.headers.get("authorization") or conn.headers.get("Authorization")
            # if auth is None:
            #     raise AuthenticationError('Invalid authentication credentials')
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            TokenVerifier(token).verify()
            return AuthCredentials(["authenticated"]), SimpleUser("adm")
        except (HTTPException, ValueError, UnicodeDecodeError, AttributeError):
            raise AuthenticationError('Invalid authentication credentials')


class TokenVerifier:
    def __init__(self, token):
        self.token = token

    def verify(self):
        if not self.token == "1234":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    user_dict = crud.get_user(db, username)
    if user_dict is not None:
        return user_dict


def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user(db, username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidTokenException()
        token_data = TokenData(username=username)
    except JWTError:
        raise InvalidTokenException()
    return token_data


async def get_current_active_user(current_user: Annotated[schemas.UserBase, Depends(get_current_user)]):
    return current_user
