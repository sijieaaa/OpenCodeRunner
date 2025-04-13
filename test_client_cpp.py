from typing import Literal

from python.run import run_python_run_info

import shutil
import os
import random
import string
import dotenv

dotenv.load_dotenv()


TMP_ROOT = os.getenv("TMP_ROOT")

def rm_makedirs(dir_path: str):
    """
    Remove a directory and all its contents.
    """
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)



class OpenCodeRunner:
    def __init__(self):
        None

    def run(self,
            run_info: dict,
            ):
        language = run_info["language"]
        language = language.lower().strip()
        root_dir = run_info["root_dir"]

        # Create a temporary directory for the session
        session_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        session_dir = os.path.join(TMP_ROOT, session_name)

        # Update the `root_dir` to include the session name. So the structure will be:
        # TMP_ROOT 
        #   |-session_dir
        #     |-root_dir
        root_dir = os.path.join(TMP_ROOT, session_name, root_dir)
        rm_makedirs(root_dir)
        run_info["root_dir"] = root_dir
 
        # Update each `file_info` in `file_infos` to include the `root_dir`
        for i in range(len(run_info["file_infos"])):
            run_info['file_infos'][i]['file_root_dir'] = root_dir

        if language in ["python", "py"]:
            process_result = run_python_run_info(run_info=run_info)
        # TODO: Add support for c++
        elif language in ["cpp", "c++"]:
            pass
        # TODO: Add support for java
        elif language in ["java", "javac"]:
            pass
        # TODO: Add support for javascript
        elif language in ["javascript", "js"]:
            pass
        # TODO: Add support for typescript
        elif language in ["typescript", "ts"]:
            pass
        # TODO: Add support for dafny
        elif language in ["dafny","dfy"]:
            pass
        else:
            raise NotImplementedError
        
        # Clean up the temporary directory
        shutil.rmtree(session_dir)
        print(process_result)
        
        return process_result



        
if __name__ == "__main__":

    # python example
    opencr = OpenCodeRunner()

    run_info = {
        "file_infos": [
            {
                "file_relpath": "file1.py",
                "file_content": """
def main1():
    print("Hello World")
    return 0
"""
            },
            {
                "file_relpath": "file2.py",
                "file_content": """
import file1
from file1 import main1
def main2():
    output = main1()
    return output
if __name__ == "__main__":
    main2()
"""
            }
        ],
        "language": "python",
        "root_dir": "zproj1/",
        "entry_file_relpath": "file2.py",
        "entry_func_name": "main2", # [str, None/Literal["__main__"]]
        # "entry_func_args": [arg1, arg2], # list
        # "entry_func_kwargs": {"key1": value1, "key2": value2}, # dict
        "entry_func_args": [], # list
        "entry_func_kwargs": {}, # dict
    }

    opencr.run(
        run_info
    )


