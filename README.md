<div align="center">
  <img src="https://github.com/OpenCodeRunner/OpenCodeRunner/blob/main/assets/opencoderunner_v3_marginborder.png" alt="OpenCodeRunner Logo" width="200"/>
  <br>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/blob/main/LICENSE">
    <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
</div>


# OpenCodeRunner
A fully open-source, free, and safe code runner that runs project-level (multi-file) code on both local machines and remote servers. It supports languages including `Python` `JavaScript/TypeScript` `C/C++` `Java` `Dafny` `Bash` etc.

OpenCodeRunner can be used in many ways:
- LLM/Agent training
- RL training
- Code evaluation
- Safe sandbox running
- Multi-language running
- Cloud or remote code running
- ...
## Installation
1. Install OpenCodeRunner
```bash
# Install
git clone https://github.com/OpenCodeRunner/OpenCodeRunner
cd OpenCodeRunner
pip install -e .

# Uninstall
pip uninstall opencoderunner 
```
2. Install Firejail sandbox for safety control (https://github.com/netblue30/firejail)
```bash
# Install via `apt`
sudo add-apt-repository ppa:deki/firejail
sudo apt-get update
sudo apt-get install firejail firejail-profiles

# Or install via building manually
git clone https://github.com/netblue30/firejail.git
cd firejail
./configure && make && sudo make install-strip
```

## Usage
OpenCodeRunner supports 2 ways of running codes: 
- Run on local machines via Python function calling
- Run on remote servers via FastAPI Web Server. Of course, you can also use this to run on local machines

#### 1. Run on Local Machines
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

#### 2. Run on Remote Servers
To run on remote servers, firstly you need to start FastAPI on your remote/cloud servers using `opencoderunner-start-server`. This command wraps `uvicorn` to launch the FastAPI server.

```Bash
opencoderunner-start-server --host 0.0.0.0 --port 8000 --reload
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
- [x] Sandbox for permission control
- [x] User
- [ ] .env config
- [ ] Project structure visualization
- [ ] Input/argparse/stdin 
- [ ] Blocking mode


## Supported Languages
- [x] Python
- [x] JavaScript
- [x] TypeScript
- [ ] C
- [ ] C++
- [x] Java
- [ ] Dafny
- [x] Bash
- ...


## Update
- [2025-04-11] Support basic cpp, javascript, python


## Contributors
😊 We welcome passionate contributors! If you are interested, feel free to contact!

[![Contributors](https://contrib.rocks/image?repo=OpenCodeRunner/OpenCodeRunner)](https://github.com/OpenCodeRunner/OpenCodeRunner/graphs/contributors)

