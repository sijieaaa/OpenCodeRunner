from opencoderunner.run_info import RunInfo
from opencoderunner.file_info import FileInfo
from opencoderunner import run

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
        project_root_name="project_root_name",                   
        entry_file_relpath="file2.py",
        input_content="INPUT1\nINPUT2\n",
    )                            

    # -- Run locally
    for i in range(3):
        result_info = run(run_info=run_info)
        print(result_info)


    # -- Or Run on server
    for i in range(3):
        result_info = run(run_info=run_info,
                        host="0.0.0.0",
                        port=8000,
                        )
        print(result_info)