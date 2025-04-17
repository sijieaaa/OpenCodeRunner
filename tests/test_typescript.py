




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.languages.info import RunInfo, FileInfo



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
        use_firejail=True,
    )


    process_result_dict = run_on_local(run_info=run_info)
    a=1