




import os
from opencoderunner.languages.info import RunInfo, FileInfo

from opencoderunner.run_on_local import run as run_on_local



if __name__ == "__main__":


    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="file1.py",
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
import file1
from file1 import main1
def main2(a:str,b=1):
    output = main1()
    output = f"{a}-{b}-{output}"
    print(output)
    return output
if __name__ == "__main__":
    main2("abc", b=123)
"""
            )
        ],
        language="python",
        project_root_name="zproj1",
        entry_file_relpath="file2.py",
        use_firejail=True,
    )
    run_info.print_tree()
    process_result_dict = run_on_local(run_info=run_info)
    a=1