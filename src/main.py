import uvicorn

from controller import app_controller

if __name__ == "__main__":
    uvicorn.run(app_controller, host="0.0.0.0", port=80)
