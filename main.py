import secrets
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from typing import Annotated
from app.routers import auth, products, jasa

load_dotenv()

app = FastAPI(
    title="Marketplace API", 
    version="1.0.0", 
    docs_url=None, 
    redoc_url=None, 
    openapi_url=None
)

security = HTTPBasic()

def authenticate_dev(credentials: HTTPBasicCredentials = Depends(security)):
    env_user = os.getenv("DOCS_USERNAME")
    env_pass = os.getenv("DOCS_PASSWORD")

    correct_username = secrets.compare_digest(credentials.username, env_user or "")
    correct_password = secrets.compare_digest(credentials.password, env_pass or "")
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Akses Dokumentasi Ditolak",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "https://fastapi-backend-marketplace.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def get_documentation(username: Annotated[str, Depends(authenticate_dev)]):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Private Docs"
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(username: Annotated[str, Depends(authenticate_dev)]):
    return get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

app.include_router(products.router)
app.include_router(auth.router)
app.include_router(jasa.router)

@app.get("/api/status")
def get_status():
    return {"status": "API is running"}