

import os
import opencoderunner
# from opencoderunner.infos.run_info import RunInfo
# from opencoderunner.infos.result_info import ResultInfo
# from opencoderunner.infos.file_info import FileInfo

from opencoderunner import RunInfo
from opencoderunner import run as opencr_run 

from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.run_on_server import run as run_on_server





if __name__ == "__main__":

    run_info = RunInfo(
        code_str="""
whoami
echo "Hello World!!!"
echo ${USER}
printf "hello world\\n" | bash -c 'read line; echo "received: $line"'
# nvidia-smi
ls -al
""",
        language="bash",
        project_root_name="zproj1", 
        delete_after_run=True
    )
    
    
    result_info = opencr_run(run_info=run_info)
    print(result_info)