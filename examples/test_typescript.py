




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo



if __name__ == "__main__":



    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="folder1/helper.ts",
                file_content="""
export function greet(name: string): string {
    return `Hello, ${name}!`;
}

"""
            ),
            FileInfo(
                file_relpath="main.ts",
                file_content="""
import { greet } from './folder1/helper';

const name = 'TS Developer';
console.log(greet(name));
"""
            )
        ],
        language="typescript",
        project_root_name="project_typescript",
        entry_file_relpath="main.ts",
        ts_node_path="/home/runner/Tools/node-v22.14.0-linux-x64/bin/ts-node",
        delete_after_run=False
    )
    run_info.print_tree()

    result_info = run_on_local(run_info=run_info)
    print(result_info)
    print(result_info.stdout)
    
    a=1