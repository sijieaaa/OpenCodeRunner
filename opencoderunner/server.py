from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import argparse

from opencoderunner.run_on_local import run as run_on_local

from opencoderunner.languages.info import RunInfo, FileInfo
from opencoderunner.languages.result_info import ResultInfo



app = FastAPI()

@app.get("/")
async def service_root():
    return_dict = {
        "message": "🚀 OpenCodeRunner is running!",
        "usage": "Send POST to /run with proper `run_info` JSON."
    }
    return return_dict


@app.post("/run", response_model=ResultInfo)
async def service_run(run_info: RunInfo):
    result_info = run_on_local(run_info=run_info)
    return result_info




def start_server(host: str = "localhost", port: int = 8000):
    """
    Start the FastAPI server on the specified `host` and `port`.
    """
    parser = argparse.ArgumentParser(description="Start OpenCodeRunner FastAPI server")
    parser.add_argument("--host", type=str, default=host, help="Host address")
    parser.add_argument("--port", type=int, default=port, help="Port number")
    opt = parser.parse_args()
    # Override default host and port with command line arguments
    host = opt.host
    port = opt.port
    print(f"FastAPI server {host}:{port}")
    uvicorn.run(app, host=host, port=port)



if __name__ == "__main__":

    start_server(host="0.0.0.0", port=8000)

    # uvicorn server:app --host 0.0.0.0 --port 8000 --reload