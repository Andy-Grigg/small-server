from fastapi import FastAPI

from .api import router as api_router
from .ui import router as ui_router

app_controller = FastAPI()
app_controller.include_router(
    api_router, prefix="/api",
)
app_controller.include_router(
    ui_router, prefix="",
)
