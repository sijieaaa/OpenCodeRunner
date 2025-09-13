




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo



if __name__ == "__main__":


    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="src/utils.js",
                file_content="""
// src/utils.js
function greet(name) {
    return `Hello, ${name}!`;
}
module.exports = {
    greet,
};
"""
            ),
            FileInfo(
                file_relpath="index.js",
                file_content="""
// index.js
const { greet } = require('./src/utils');
const name = 'JavaScript with folder';
console.log(greet(name));
"""
            )
        ],
        language="javascript",
        project_root_name="project_javascript", 
        entry_file_relpath="index.js",
        node_path="/home/runner/Tools/node-v22.14.0-linux-x64/bin/node", 
    )
    run_info.print_tree()


    result_info = run_on_local(run_info=run_info)
    print(result_info)
    print(result_info.stdout)
    print(result_info.stdout.decode())

    a=1