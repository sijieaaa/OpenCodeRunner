

import os
from opencoderunner.run_on_local import run as run_on_local





if __name__ == "__main__":
    run_info = {
        "file_infos": [],
        "bash_command": """pwd
whoami
echo "Hello World!!!"
echo ${HOME}
""",
        "language": "bash",
        "project_root_name": "zproj1", 

        # -- (Optional) Specify the bash path
        "bash_path": "/usr/bin/bash", # default: "bash"

        # -- (Optional) You can specify the user to run the code
        # "user": "runner", # str or None
        "user": None, # str or None

        # -- (Optional) Whether to use Firejail sandbox
        "use_firejail": False, # bool

    }


    
    run_on_local(run_info=run_info)
    a=1