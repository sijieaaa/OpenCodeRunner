<div align="center">
  <img src="https://github.com/OpenCodeRunner/OpenCodeRunner/blob/main/assets/opencoderunner_v3_marginborder.png" alt="OpenCodeRunner Logo" width="200"/>
  <br>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/blob/main/LICENSE">
    <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
</div>


# OpenCodeRunner
A fully open-source code runner that executes project-level (multi-file) code locally or via a server, supporting languages including `Python` `Javascript/Typescript` `C/C++` `Java` `Dafny` etc.
## Installation
```bash
# Install
git clone https://github.com/OpenCodeRunner/OpenCodeRunner
cd OpenCodeRunner
pip install -e .

# Uninstall
pip uninstall opencoderunner 
```
## Usage
OpenCodeRunner supports 2 ways of running codes: 
- Run on local machines via Python function calling
- Run on remote servers via FastAPI Web Server. Of course, you can also use this to run on local machines

#### Run on local machines
You can easily use `run_on_local` to obtain the results
```Python
from opencoderunner.run_on_local import run as run_on_local

run_info = {
    "file_infos": [
        {
            "file_relpath": "file1.py", # i.e. f"{project_root_name}/file1.py"
            "file_content": """
def main1():
print("Hello World")
return 123
"""
        },
        {
            "file_relpath": "file2.py", # i.e. f"{project_root_name}/file2.py"
            "file_content": """
import file1
from file1 import main1
def main2(a:str,b=1):
output = main1()
output = f"{a}-{b}-{output}"
return output
if __name__ == "__main__":
main2()
"""
        }
    ],
    "language": "python",
    "project_root_name": "zproj1", 
    "entry_file_relpath": "file2.py",
    "entry_func_name": "main2", # [str, None]
    "entry_func_args": ["abc"], # list
    "entry_func_kwargs": {"b": 123}, # dict
}
# Run on local machines
process_result_dict_local = run_on_local(run_info)           
print(process_result_dict_local)  
```

#### Run on remote servers
To run on remote servers, you need first start the FastAPI Web Server using `opencoderunner-start-server`

```Bash
opencoderunner-start-server --host 0.0.0.0 --port 8000
```

Then, you need to specify `host` and `port` in `run_on_server` to run on remote servers

```Python
from opencoderunner.run_on_local import run as run_on_server
from opencoderunner.server import start_server

run_info # You can copy from the local running example

# Run on remote servers
host = "0.0.0.0"
port = 8000
process_result_dict_server = run_on_server(
    run_info,
    host=host,
    port=port    
)       
print(process_result_dict_server)  
```

## TODO
- [ ] Sandbox 

## Supported Languages
- [x] Python
- [ ] JavaScript
- [ ] TypeScript
- [ ] C
- [ ] C++
- [ ] Java
- [ ] Dafny


## Update

### 2025-04-11
- Support basic cpp, javascript, python


## Contributors

[![Contributors](https://contrib.rocks/image?repo=OpenCodeRunner/OpenCodeRunner)](https://github.com/OpenCodeRunner/OpenCodeRunner/graphs/contributors)

