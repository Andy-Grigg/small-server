import threading
import time

import uvicorn
from fastapi import FastAPI

file_server = FastAPI()


class FileServer(uvicorn.Server):
    _thread: threading.Thread

    def install_signal_handlers(self):
        pass

    def start(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.start()
        while not self.started:
            time.sleep(1e-3)
        return

    def stop(self):
        self.should_exit = True
        self._thread.join()


fileserver_config = uvicorn.Config(
    "server:file_server",
    host="0.0.0.0",
    port=8080,
    log_level="debug",
)


@file_server.get("/files")
def list_files():
    return "All my files!"
