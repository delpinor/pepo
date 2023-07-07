from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/version")
def version():
    return {"version": "0.0.1"}
