import typing
from typing import Literal


run_info = {
    "file_infos": [],



    "language": "dafny",
    "project_root_name": "project_dafny", 
    
    "entry_file_relpath": "Main.dfy",
    



    # -- (Optional) You can specify the user to run the code
    # Make sure the user has necessary code-related environments.
    "user": "user123",

    # -- (Optional) Whether to use Firejail sandbox.
    # This will make some folders invisible.
    "use_firejail": bool, # bool

    # -- bash
    "bash_path": str, # "/usr/bin/bash"
    "bash_command": str, # "echo hello world"


    # -- dafny
    "dafny_path": str,

    # -- java
    "java_path": str,
    "javac_path": str,

    # -- javascript
    "node_path": str,

    # -- python
    "python_path": str, 
    
    # -- typescript
    "ts_node_path": str,
    
}