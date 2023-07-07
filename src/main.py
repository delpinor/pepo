from fastapi import FastAPI

from .routers import router
app = FastAPI()


# Routers
app.include_router(router)


@app.get("/")
def root():
    return {"message": "it's alive"}
