from pydantic import BaseModel, ConfigDict
from pydantic import model_validator
from typing import Optional, Literal, Any
import warnings
from collections import defaultdict
from opencoderunner.file_info import FileInfo
import os

class RunInfo(BaseModel):
    # model_config = ConfigDict(extra="allow") # Allow adding extra fields after initialization.

    file_infos: Optional[list[FileInfo]] = [] # List of file information. 
    code_str: Optional[str] = None # Code string. 
    language: Literal[
        "bash",
        "dafny", "dfy",
        "java", "javac",
        "javascript", "js",
        "python", "py",
        "typescript", "ts",
        "sql", "postgres", "postgresql",
    ]
    # tmp_root: Optional[str] = "/tmp" # Can change to your own temporary root.
    tmp_root: Optional[str] = os.path.join(os.environ["HOME"], "tmp")
    os.makedirs(tmp_root, exist_ok=True) # Ensure the temporary root directory exists.
    session_name: Optional[str] = None # Session name. If not provided, a random name will be generated.
    project_root_name: Optional[str] = None 

    session_dir: Optional[str] = None # Session directory. If not provided, a random name will be generated.
    project_root_dir: Optional[str] = None # Project root directory. If not provided, a random name will be generated.

    entry_file_relpath: Optional[str] = None # Optional for bash. Required for all other languages.
    entry_file_abspath: Optional[str] = None # Absolute path of the entry file. Optional for bash. Required for all other languages.
    input_content: Optional[Any] = None # Input for the entry function. Optional for bash. Required for all other languages.


    user: Optional[str] = None # Testing
    use_firejail: Optional[bool] = False
    use_shell: Optional[bool] = True

    # tmp_root: Optional[str] = "/home/runner/Tools/OpenCodeRunner/tmp"
    delete_after_run: Optional[bool] = True # Delelte the created temporary files after run.
    timeout: Optional[float] = 60 # Timeout for the run. Default is 60 seconds.
    ram_limit_gb: Optional[float] = 8.0 # RAM limit in GB. Default is 4GB.
    is_quick_run: bool = False 

    command: Optional[str] = None 
    pre_command: Optional[str] = "" # Pre command to run before the main command. Useful for setting environment variables or other preparations.

    # -- bash
    bash_path: Optional[str] = "bash"

    # -- dafny
    dafny_path: Optional[str] = "dafny"

    # -- java
    java_path: Optional[str] = "java"
    javac_path: Optional[str] = "javac"

    # -- javascript
    node_path: Optional[str] = "node"

    # -- python
    python_path: Optional[str] = "python3"
    entry_func_name: Optional[str] = None
    entry_func_args: Optional[list] = []
    entry_func_kwargs: Optional[dict] = {}

    # -- typescript
    ts_node_path: Optional[str] = "ts-node"

    # -- sql
    psql_path: Optional[str] = "psql"
    

    # def __setattr__(self, key, value):
    #     super().__setattr__(key, value)  
    #     if key not in self.model_fields:
    #         self.__dict__[key] = value


    @model_validator(mode='after')
    def check(self):
        # if self.language in ["bash"]:
        #     assert self.input_content is None, f"`input_content` is not supported for {self.language}."

        if self.user is not None:
            warnings.warn(f"`user` option is still not fully supported. It may not work as expected.")

        if (self.code_str is not None) and (len(self.file_infos) > 0):
            raise ValueError("`code_str` and `file_infos` cannot be used together. Please use one of them.")
        if (self.code_str is None) and (len(self.file_infos) == 0):
            raise ValueError("`code_str` or `file_infos` must be provided. Please use one of them.")
        

        return self
    
    def print_tree(self):
        from collections import defaultdict

        # Build the tree structure
        tree = lambda: defaultdict(tree)
        root = tree()
        for file_info in self.file_infos:
            parts = file_info.file_relpath.strip("/").split("/")
            current = root
            for part in parts:
                current = current[part]

        # Print the tree structure
        def _print(current, prefix=""):
            items = sorted(current.items())
            for i, (name, subtree) in enumerate(items):
                connector = "└── " if i == len(items) - 1 else "├── "
                print(f"{prefix}{connector}{name}")
                next_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
                _print(subtree, next_prefix)

        # Print the root directory
        print("===== Directory Tree =====")
        print(f"{self.project_root_name}/")
        _print(root)
        print("==========================")

    def print_command(self):
        print("===== Command =====")
        print(self.command)
        print("===================")