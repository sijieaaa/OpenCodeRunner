
import dotenv
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.run_on_server import run as run_on_server
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo

if __name__ == "__main__":
    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="folder1/file1.py",
                file_content="""
def main1():
    import numpy as np
    arr = np.array([1, 2, 3])
    print("Hello World")
    output = arr.sum()
    return output
"""
            ),
            FileInfo(
                file_relpath="file2.py",
                file_content="""
from folder1.file1 import main1
import sys
import json

print(main1())
for line in sys.stdin:
    line = line.strip()
    print(line)
"""
            )
        ],
        language="python",
        project_root_name="zproj1",                   
        entry_file_relpath="file2.py",
        input_content="INPUT1\nINPUT2\n",
        delete_after_run=False
    )                               
    run_info.print_tree()

    # -- Run locally
    result_info = run_on_local(run_info=run_info)
    print(result_info)
    print(result_info.stdout.decode())

    # -- is_run=False
    run_info = run_on_local(
        run_info=run_info,
        is_run=False
    )
    print(run_info)

    # -- Or Run on server
    result_info = run_on_server(run_info=run_info,
                                host="0.0.0.0",
                                port=8000,
                                api_key="12345",
                                # You can set Server/Client API keys in `.env`
                                # api_key=dotenv.get_key(".env", "OPENCODERUNNER_API_KEY") 
                                )
    print(result_info)
    print(result_info.stdout.decode())