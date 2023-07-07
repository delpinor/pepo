from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .routers import router
app = FastAPI()


# Routers
app.include_router(router)


@app.get("/")
def root():
    return RedirectResponse("/version")
