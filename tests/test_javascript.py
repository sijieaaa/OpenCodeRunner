




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.languages.info import RunInfo, FileInfo



if __name__ == "__main__":



#     run_info = {
#         "file_infos": [
#             {
#                 "file_relpath": "src/utils.js", # i.e. f"{project_root_name}/file1.py"
#                 "file_content": """
# // src/utils.js
# function greet(name) {
#     return `Hello, ${name}!`;
# }

# module.exports = {
#     greet,
# };
# """
#             },
#             {
#                 "file_relpath": "index.js", # i.e. f"{project_root_name}/file2.py"
#                 "file_content": """
# // index.js
# const { greet } = require('./src/utils');

# const name = 'JavaScript with folder';
# console.log(greet(name));

# """
#             }
#         ],
#         "language": "javascript",
#         "project_root_name": "project_javascript", 
#         "entry_file_relpath": "index.js",
        
#         # -- (Optional) Specify the node path
#         "node_path": "/home/runner/Tools/node-v22.14.0-linux-x64/bin/node", 


#         # -- (Optional) Whether to use Firejail sandbox
#         "use_firejail": False, # bool
#     }


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
        use_firejail=True, # bool
    )


    process_result_dict = run_on_local(run_info=run_info)
    a=1