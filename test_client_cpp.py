








from typing import Literal

from opencoderunner.languages.python.run import run_python_run_info
from opencoderunner.languages.cpp.run import run_cpp_run_info

import shutil
import os
import random
import string
import dotenv

dotenv.load_dotenv()


TMP_ROOT = os.getenv("TMP_ROOT")

def rm_makedirs(dir_path: str):
    """
    Force to remove a directory. And then create a clean one.
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
        root_folder_name = run_info["root_folder_name"]

        # Create a temporary directory for the session
        session_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        session_dir = os.path.join(TMP_ROOT, session_name)

        # Update the `root_dir` to include the session name. So the structure will be:
        # TMP_ROOT 
        #   |-session_name
        #      |-root_folder_name
        root_dir = os.path.join(TMP_ROOT, session_name, root_folder_name)
        rm_makedirs(root_dir)
        run_info["root_dir"] = root_dir
 
        # Update each `file_info` in `file_infos` to include the `root_dir`
        for i in range(len(run_info["file_infos"])):
            run_info['file_infos'][i]['file_root_dir'] = root_dir

        if language in ["python", "py"]:
            process_result = run_python_run_info(run_info=run_info)
        elif language in ["cpp", "c++"]:
            # TODO: Add support for c++
            # NOTE: Need to support `compiler` config.
            #       Be careful about single quote `''` and double quote `""` in C/C++
            process_result = run_cpp_run_info(run_info=run_info)
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
                "file_relpath": "file1.cpp",
                "file_content": """
#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
    return 0;
}
"""
            },
        ],
        "language": "c++",
        "compiler": "g++",
        "root_folder_name": "zproj1",
        "entry_file_relpath": None, # str
        "entry_func_name": None, # str
        # "entry_func_args": [arg1, arg2], # list
        # "entry_func_kwargs": {"key1": value1, "key2": value2}, # dict
        "entry_func_args": [], # list
        "entry_func_kwargs": {}, # dict
    }

    process_result = opencr.run(
        run_info
    )                            

    None

    



