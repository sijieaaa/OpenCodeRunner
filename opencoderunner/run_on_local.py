from typing import Literal

from opencoderunner.languages.python.run import run_python_run_info

import shutil
import os
import random
import string
import json
import os
import dotenv
dotenv.load_dotenv()


TMP_ROOT = os.getenv("TMP_ROOT")
READONLY_DIRS = os.getenv("READONLY_DIRS")
WRITABLE_DIRS = os.getenv("WRITABLE_DIRS")


print("TMP_ROOT:", TMP_ROOT)
print("READONLY_DIRS:", READONLY_DIRS)
print("WRITABLE_DIRS:", WRITABLE_DIRS)


def rm_makedirs(dir_path: str):
    """
    Force to remove a directory. And then create a clean one.
    """
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)



def run(
        run_info: dict,
    ):
    language = run_info["language"]
    language = language.lower().strip()
    project_root_name = run_info["project_root_name"]

    # Create a temporary directory for the session
    session_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    session_dir = os.path.join(TMP_ROOT, session_name)
    rm_makedirs(session_dir)
    run_info["session_dir"] = session_dir


    # Update the `root_dir` to include the session name. So the structure will be:
    # TMP_ROOT 
    #   |-session_name
    #      |-project_root_name
    project_root_dir = os.path.join(TMP_ROOT, session_name, project_root_name)
    rm_makedirs(project_root_dir)
    run_info["project_root_dir"] = project_root_dir

    # Update each `file_info` in `file_infos` to include the `project_root_dir`
    for i in range(len(run_info["file_infos"])):
        file_abspath = os.path.join(project_root_dir, run_info['file_infos'][i]['file_relpath'])
        run_info['file_infos'][i]['file_abspath'] = file_abspath
 

    # Include `entry_file_abspath`
    run_info["entry_file_abspath"] = os.path.join(project_root_dir, run_info["entry_file_relpath"])


    if language in ["python", "py"]:
        process_result = run_python_run_info(run_info=run_info)
    else:
        raise NotImplementedError
    
    # Clean up the temporary directory
    shutil.rmtree(session_dir)
    print(process_result)

    process_result_dict = process_result.to_dict()    
    return process_result_dict



        
if __name__ == "__main__":




    run_info = {
        "file_infos": [
            {
                "file_relpath": "file1.py", # i.e. f"{project_root_name}/file1.py"
                "file_content": """
def main1():
    print("Hello World")
    return 123
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
    return output
if __name__ == "__main__":
    main2("abc", b=123)
"""
            }
        ],
        "language": "python",
        "project_root_name": "zproj1", 
        "entry_file_relpath": "file2.py",

        # You can also specify entry function as belows
        
        # "entry_func_name": "main2", # [str, None/Literal["__main__"]]
        # "entry_func_args": ["abc"], # list
        # "entry_func_kwargs": {"b": 123}, # dict
    }
    process_result_dict = run(
        run_info
    )           
    print(process_result_dict)              

