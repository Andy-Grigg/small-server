import time
from fastapi import APIRouter, BackgroundTasks

from server import FileServer, fileserver_config

_server: FileServer | None = None
router = APIRouter()

_time_remaining = None


def shutdown_server_after_time(time_to_shutdown: int):
    global _time_remaining

    _time_remaining = time_to_shutdown
    while _time_remaining > 0:
        time.sleep(60)
        _time_remaining = _time_remaining - 1
    stop_server()
    _time_remaining = None


@router.get("/server")
def server_status():
    global _time_remaining
    if _time_remaining == -1:
        return "Server running forever"
    elif _time_remaining:
        return f"{_time_remaining} minutes remaining"
    return "Server not running"


@router.get("/server/start")
async def start_server(background_tasks: BackgroundTasks, time_to_shutdown: int = 0):
    global _server
    global _time_remaining

    if _server and _time_remaining == -1:
        return "Server running forever"
    if _server and _time_remaining:
        return f"{_time_remaining} minutes remaining"

    _server = FileServer(config=fileserver_config)
    _server.start()
    if not time_to_shutdown:
        _time_remaining = -1
        return "Server running forever"
    else:
        background_tasks.add_task(shutdown_server_after_time, time_to_shutdown)
        return f"{time_to_shutdown} minutes remaining"


@router.get("/server/stop")
def stop_server():
    global _server
    global _time_remaining

    if _server:
        _server.stop()
        _server = None
        _time_remaining = None
    return "Server not running."
