from fastapi import APIRouter

from server import FileServer, fileserver_config

_server: FileServer | None = None
router = APIRouter()


@router.get("/server")
def server_status():
    return "Running" if _server else "Stopped"


@router.get("/server/start")
def start_server(time_to_shutdown: int = 45):
    global _server
    if _server:
        return f"Server already running on port {_server.config.port}."
    _server = FileServer(config=fileserver_config)
    _server.start()
    return f"Server running on port {_server.config.port}"


@router.get("/server/stop")
def stop_server():
    global _server
    if _server:
        _server.stop()
        _server = None
    return "Server stopped"
