from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import argparse

from opencoderunner.run_on_local import run as run_on_local



class FileInfo(BaseModel):
    file_relpath: str
    file_content: str



class RunInfo(BaseModel):
    file_infos: List[FileInfo]
    language: str
    project_root_name: str
    entry_file_relpath: str
    entry_func_name: Optional[str] = None
    entry_func_args: Optional[List[Any]] = []
    entry_func_kwargs: Optional[Dict[str, Any]] = {}



app = FastAPI()



@app.get("/")
async def service_root():
    return_dict = {
        "message": "🚀 OpenCodeRunner is running!",
        "usage": "Send POST to /run with proper `run_info` JSON."
    }
    return return_dict


@app.post("/run")
async def service_run(run_info_obj: RunInfo):
    run_info_dict = run_info_obj.dict()
    process_result_dict = run_on_local(run_info=run_info_dict)
    return process_result_dict



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