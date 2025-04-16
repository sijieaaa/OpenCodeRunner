




import os
from opencoderunner.run_on_local import run as run_on_local



if __name__ == "__main__":



    run_info = {
        "file_infos": [
            {
                "file_relpath": "src/utils.js", # i.e. f"{project_root_name}/file1.py"
                "file_content": """
// src/utils.js
function greet(name) {
    return `Hello, ${name}!`;
}

module.exports = {
    greet,
};
"""
            },
            {
                "file_relpath": "index.js", # i.e. f"{project_root_name}/file2.py"
                "file_content": """
// index.js
const { greet } = require('./src/utils');

const name = 'JavaScript with folder';
console.log(greet(name));

"""
            }
        ],
        "language": "javascript",
        "project_root_name": "project_javascript", 
        "entry_file_relpath": "index.js",
        
        # -- (Optional) Specify the node path
        "node_path": "/home/runner/Tools/node-v22.14.0-linux-x64/bin/node", 

        # -- (Optional) You can specify the user to run the code
        # "user": "runner", # str or None
        "user": None, # str or None

        # -- (Optional) Whether to use Firejail sandbox
        "use_firejail": False, # bool
    }

    process_result_dict = run_on_local(run_info=run_info)
    a=1