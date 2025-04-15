

import os
from opencoderunner.run_on_local import run as run_on_local





if __name__ == "__main__":
    run_info = {
        "file_infos": [],
        "bash_command": """
pwd
whoami
""",
        "language": "bash",
        "project_root_name": "zproj1", 
        # sudo visudo
        # Add the following line into the opened file
        # sudo ALL=(tmp_user) NOPASSWD: ALL
        # "username": "tmp_user",
    }


    
    run_on_local(run_info=run_info)
    a=1