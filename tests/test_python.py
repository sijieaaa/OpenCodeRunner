




import os
from opencoderunner.run_on_local import run as run_on_local



if __name__ == "__main__":



    run_info = {
        "file_infos": [
            {
                "file_relpath": "file1.py", # i.e. f"{project_root_name}/file1.py"
                "file_content": """
def main1():
    import numpy as np
    arr = np.array([1, 2, 3])
    print("Hello World")
    output = arr.sum()
    return output
"""
            },
            {
                "file_relpath": "file2.py", # i.e. f"{project_root_name}/file2.py"
                "file_content": """
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
            }
        ],
        "language": "python",
        "project_root_name": "zproj1", 
        "entry_file_relpath": "file2.py",
        # python
        # /home/runner/miniconda3/bin/python
        # /home/runner/miniconda3/envs/tmp-python3.10/bin/python
        "python_path": "/home/runner/miniconda3/envs/tmp-python3.10/bin/python", 

        # -- Uncomment belolws. You can also specify entry function as belows
        # "entry_func_name": "main2", # [str, None/Literal["__main__"]]
        # "entry_func_args": ["abc"], # list
        # "entry_func_kwargs": {"b": 123}, # dict
    }

    process_result_dict = run_on_local(run_info=run_info)
    a=1