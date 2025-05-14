

from opencoderunner.file_info import FileInfo
from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.run_on_server import run as run_on_server


from typing import Optional, Literal

def run(
    run_info: RunInfo,
    is_run: bool = True,
    host: Optional[str] = None,
    port: Optional[int] = None,
    api_key: Optional[str] = "12345",
    mode: Optional[Literal["bytes", "msgpack"]] = "msgpack",
):
    # -- Server
    if host is not None and port is not None:
        result_info = run_on_server(
            run_info=run_info,
            host=host,
            port=port,
            api_key=api_key,
            mode=mode
        )
        return result_info
    
    # -- Local
    if host is None or port is None:
        result_info = run_on_local(
            run_info=run_info,
            is_run=is_run
        )
        return result_info