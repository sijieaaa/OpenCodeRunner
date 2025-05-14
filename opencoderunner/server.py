from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import argparse
import pickle
import msgpack
import dotenv
import os

from opencoderunner.run_on_local import run as run_on_local

from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.file_info import FileInfo


app = FastAPI()
# Load `.env` file for API keys
trusted_api_keys = dotenv.get_key(".env", "TRUSTED_OPENCODERUNNER_API_KEYS")
trusted_api_keys = trusted_api_keys.split(",") if trusted_api_keys else []



def verify_api_key(api_key: str):
    """
    Verify the API key against the trusted keys.
    """
    if api_key not in trusted_api_keys:
        raise ValueError("Invalid API key")


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


@app.post("/run_bytes")
async def service_run_bytes(request: Request):
    api_key = request.headers.get("api_key")
    if api_key not in trusted_api_keys:
        response = Response(
            content="Invalid api_key",
            media_type="text/plain",
            status_code=401
        )
        return response
    raw = await request.body()
    run_info = pickle.loads(raw)
    run_info = RunInfo.model_validate(run_info)
    result_info = run_on_local(run_info)
    result_bytes = pickle.dumps(result_info)
    response = Response(
        content=result_bytes,
        media_type="application/octet-stream"
    )
    return response


@app.post("/run_msgpack")
async def service_run_msgpack(request: Request):
    api_key = request.headers.get("api_key")
    if api_key not in trusted_api_keys:
        response = Response(
            content="Invalid api_key".encode(),
            media_type="text/plain",
            status_code=401
        )
        return response
    raw = await request.body()
    run_info = msgpack.unpackb(raw, raw=False)
    run_info = RunInfo.model_validate(run_info)
    result_info = run_on_local(run_info)
    result_bytes = msgpack.packb(result_info.model_dump(), use_bin_type=True)
    response = Response(
        content=result_bytes,
        media_type="application/msgpack"
    )
    return response


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