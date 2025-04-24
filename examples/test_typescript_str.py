




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo



if __name__ == "__main__":



    run_info = RunInfo(
        code_str="""console.log("Hello from TypeScript!");""",
        language="typescript",
        project_root_name="project_typescript",
        ts_node_path="/home/runner/Tools/node-v22.14.0-linux-x64/bin/ts-node",
    )
    run_info.print_tree()

    result_info = run_on_local(run_info=run_info)
    print(result_info)
    print(result_info.stdout)
    
    a=1