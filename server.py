from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


from test_client_python import OpenCodeRunner  



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
opencr = OpenCodeRunner()



@app.get("/")
async def service_root():
    return_dict = {
        "message": "🚀 OpenCodeRunner is running!",
        "usage": "Send POST to /run with proper `run_info` JSON."
    }
    return return_dict


@app.post("/run")
async def service_run(run_info: RunInfo):
    run_info_dict = run_info.dict()
    process_result = opencr.run(run_info_dict)
    process_result_dict = process_result.to_dict()
    return process_result_dict

# uvicorn server:app --host 0.0.0.0 --port 8000 --reload