from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from supabase import Client
from jose import JWTError, jwt

from app.config import Settings
from app.database import get_supabase_client
from ..services.authentication_service import authenticate_user, create_access_token, create_user_in_db, get_current_user, create_refresh_token
from ..models.auth_model import Token, User, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Annotated[Client, Depends(get_supabase_client)],
):
    existing_user = authenticate_user(db, user_data.username, "dummy_password")
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )

    new_user = create_user_in_db(db, user_data)

    if new_user:
        return new_user
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user due to server or database issue"
        )


@router.post("/login", response_model=Token)
async def login_for_access_token(
        user_credential: UserLogin,
        db: Annotated[Client, Depends(get_supabase_client)],
        response: Response
    ) -> Token:

    user = authenticate_user(db, user_credential.username, user_credential.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=Settings.access_token_expire_minutes)

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        # secure=True, use this in production with HTTPS
        secure=False,
        samesite="lax",
        max_age=604800
    )

    return Token(access_token=access_token, token_type="bearer")

@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: Annotated[str, Cookie()] = None):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    try:
        payload = jwt.decode(refresh_token, Settings.secret_key, algorithms=[Settings.algorithm])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    new_access_token = create_access_token(
        data={"sub": username, "role": role},
        expires_delta=timedelta(minutes=Settings.access_token_expire_minutes)
    )
    
    return Token (
        access_token=new_access_token,
        token_type="bearer"
    )


@router.get("/me", response_model=User)
async def read_current_user(
        current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
