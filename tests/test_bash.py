

import os

from opencoderunner.languages.info import RunInfo, FileInfo
from opencoderunner.run_on_local import run as run_on_local





if __name__ == "__main__":

    run_info = RunInfo(
        file_infos=[],
        bash_command="""pwd
whoami
echo "Hello World!!!"
echo ${HOME}
echo ${USER}
pwd
""",
        language="bash",
        project_root_name="zproj1", 
        use_firejail=True, # bool
    )
    run_info.print_tree()
    
    run_on_local(run_info=run_info)
    a=1