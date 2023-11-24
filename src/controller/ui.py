from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/")
def server_status():
    file_path = Path(__file__).parent / "index.html"
    with open(file_path) as f:
        return HTMLResponse(f.read())
