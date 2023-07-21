from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import RedirectResponse

from .auth import BasicAuthBackend
from .routers import router
app = FastAPI()

# Authentication
# app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(router)


@app.get("/")
def root():
    return RedirectResponse("/version")
