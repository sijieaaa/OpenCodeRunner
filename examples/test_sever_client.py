

import time
from opencoderunner.run_on_server import run as run_on_server
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo

if __name__ == "__main__":
    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="file1.py",
                file_content="""print("Hello World")"""
            ),
        ],
        language="python",
        project_root_name="zproj1",
        entry_file_relpath="file1.py",
        use_firejail=True,
    )

    host = "0.0.0.0"
    port = 8000

    result_info = run_on_server(
        run_info=run_info,
        host=host,
        port=port,
    )