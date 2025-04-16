




import os
from opencoderunner.run_on_local import run as run_on_local



if __name__ == "__main__":



    run_info = {
        "file_infos": [
            {
                "file_relpath": "folder1/helper.ts", # i.e. f"{project_root_name}/file1.py"
                "file_content": """
export function greet(name: string): string {
    return `Hello, ${name}!`;
}

"""
            },
            {
                "file_relpath": "main.ts", # i.e. f"{project_root_name}/file2.py"
                "file_content": """
import { greet } from './folder1/helper';

const name = 'TS Developer';
console.log(greet(name));
"""
            }
        ],
        "language": "typescript",
        "project_root_name": "project_typescript", 
        "entry_file_relpath": "main.ts",
        
        # -- (Optional) Specify the ts-node path
        "ts_node_path": "/home/runner/Tools/node-v22.14.0-linux-x64/bin/ts-node", 

        # -- (Optional) You can specify the user to run the code
        # "user": "runner", # str or None
        "user": None, # str or None

        # -- (Optional) Whether to use Firejail sandbox
        "use_firejail": False, # bool
    }

    process_result_dict = run_on_local(run_info=run_info)
    a=1