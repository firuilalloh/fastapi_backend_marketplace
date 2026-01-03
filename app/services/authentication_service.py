from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from supabase import Client

from app.config import Settings
from app.database import get_supabase_client
from ..models.auth_model import TokenData, User, UserInDb, UserCreate

SECRET_KEY = Settings.secret_key
ALGORITHM = Settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.access_token_expire_minutes

pass_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pass_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pass_hash.hash(password)


def create_user_in_db(db: Client, user_data: UserCreate) -> User | None:
    existing_user = get_user(db, user_data.username)
    if existing_user:
        return None

    hashed_password = get_password_hash(user_data.password)

    user_to_save = {
        "username": user_data.username,
        "email": user_data.email,
        "role": "user",
        "password": hashed_password
    }

    try:
        response = db.table("tb_user").insert(user_to_save).execute()

        if response.data:
            created_user_data = response.data[0]
            return User(
                id=created_user_data["id"],
                username=created_user_data["username"],
                email=created_user_data["email"],
                role=created_user_data.get("role", "user")
            )
        return None

    except Exception as e:
        print(f"Error creating user in Supabase: {e}")
        return None


def get_user(db: Client, username: str) -> UserInDb | None:
    try:
        response = db.table("tb_user").select("*").eq("username", username).limit(1).execute()

        if response.data and len(response.data) > 0:
            user_data = response.data[0]
            hashed_pass = user_data.get("password")
            return UserInDb(
                id=user_data.get("id"),
                username=user_data.get("username"),
                role=user_data.get("role"),
                email=user_data.get("email"),
                hashed_password=user_data.get("password")
            )
        return None
    except Exception as e:
        print(f"Error fetching user from Supabase: {e}")
        return None


def authenticate_user(db: Client, username: str, password: str) -> UserInDb | bool:
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Client, Depends(get_supabase_client)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if username is None or token_type != "access":
            raise credentials_exception
        
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return User(**user.model_dump(exclude={"hashed_password"}))


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def check_is_admin(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation requires admin privileges"
        )
    return current_user
