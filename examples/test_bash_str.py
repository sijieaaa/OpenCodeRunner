

import os
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo

from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.run_on_server import run as run_on_server





if __name__ == "__main__":

    run_info = RunInfo(
        code_str="""
whoami
echo "Hello World!!!"
echo ${USER}
printf "hello world\\n" | bash -c 'read line; echo "received: $line"'
""",
        language="bash",
        project_root_name="zproj1", 
        delete_after_run=False
    )
    run_info.print_tree()
    
    result_info = run_on_local(run_info=run_info)
    print(result_info)
    
    result_info = run_on_server(run_info=run_info,
                                host="localhost",
                                port=8000,
                                api_key="12345"
                                )
    print(result_info)

    a=1