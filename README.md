<div align="center">
  <img src="https://github.com/OpenCodeRunner/OpenCodeRunner/blob/main/assets/opencoderunner_v3_marginborder.png" alt="OpenCodeRunner Logo" width="200"/>
  <br>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/stargazers">
    <img alt="GitHub Stars" src="https://img.shields.io/github/stars/OpenCodeRunner/OpenCodeRunner?style=social">
  </a>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/issues">
    <img alt="GitHub Issues" src="https://img.shields.io/github/issues/OpenCodeRunner/OpenCodeRunner">
  </a>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/commits/main">
    <img alt="Last Commit" src="https://img.shields.io/github/last-commit/OpenCodeRunner/OpenCodeRunner">
  </a>
  <a href="https://colab.research.google.com/drive/1TyG3tdcU3UfYJKVPjP2lBiZOoZC-FEAh?usp=sharing">
    <img alt="Open In Colab" src="https://colab.research.google.com/assets/colab-badge.svg">
  </a>
</div>


# OpenCodeRunner
A fully free and open-source API that runs project-level (multi-file) code on both local machines and remote servers with sandboxes. It supports languages including `Python` `JS/TS` `C/C++` `Java` `Dafny` `Bash` etc.

OpenCodeRunner can be used in many ways:
- LLM, agent, reasoning, RL
- Project-level code evaluation
- Safe sandbox running
- Multi-language running
- Cloud or remote code running
- ...
## Installation
#### 1. Install OpenCodeRunner
```bash
# Install
git clone https://github.com/OpenCodeRunner/OpenCodeRunner
cd OpenCodeRunner
pip install -r requirements.txt
pip install -e .

# Uninstall
pip uninstall opencoderunner 
bash ./uninstall.sh
```
#### 2. (Optional) Install Firejail sandbox for safety control (https://github.com/netblue30/firejail)
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

#### 3. The installation guides for each code language's environment is in [install_envs.md](install_envs.md)


## Usage
#### 1. (Optional) Start OpenCodeRunner Service
You can use `firejail` `uvicorn` to start the OpenCodeRunner service for remotely code execution. You can configure API key settings in [.env](.env) for both client and server sides.
```bash
# Under the repo's root `OpenCodeRunner/` directory
firejail && uvicorn opencoderunner.server:app --host 0.0.0.0 --port 8000 --reload

# Or if you don't have `firejail`
uvicorn opencoderunner.server:app --host 0.0.0.0 --port 8000 --reload
```
#### 2. Running Code
Then you can use either `run_on_local` or `run_on_server` for code running.
If you use `run_on_server`, you need to specify `host` `port` `api_key`. You can configure API key settings in [.env](.env) for both client and server sides.

- Code string running example.
```python
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.run_on_server import run as run_on_server
from opencoderunner.infos.run_info import RunInfo

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="import sys; print(sys.stdin.read())",
        language="python",
        project_root_name="zproj1",  
        input_content="INPUT1\nINPUT2\n",
    )           
    run_info.print_tree()               

    # -- Run locally
    result_info = run_on_local(run_info=run_info)
    print(result_info)

    # -- Or Run on server
    result_info = run_on_server(run_info=run_info,
                                host="0.0.0.0",
                                port=8000,
                                api_key="12345"
                                )
    print(result_info)
```

- Project-level example. It consists of multiple files.
```python
import dotenv
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.run_on_server import run as run_on_server
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo

if __name__ == "__main__":
    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="folder1/file1.py",
                file_content="""
def main1():
    import numpy as np
    arr = np.array([1, 2, 3])
    print("Hello World")
    output = arr.sum()
    return output
"""
            ),
            FileInfo(
                file_relpath="file2.py",
                file_content="""
from folder1.file1 import main1
import sys
import json

print(main1())
for line in sys.stdin:
    line = line.strip()
    print(line)
"""
            )
        ],
        language="python",
        project_root_name="zproj1",                   
        entry_file_relpath="file2.py",
        input_content="INPUT1\nINPUT2\n",
        delete_after_run=False
    )                               
    run_info.print_tree()

    # -- Run locally
    result_info = run_on_local(run_info=run_info)
    print(result_info)

    # -- Or Run on server
    result_info = run_on_server(run_info=run_info,
                                host="0.0.0.0",
                                port=8000,
                                api_key="12345",
                                # You can set Server/Client API keys in `.env`
                                # api_key=dotenv.get_key(".env", "OPENCODERUNNER_API_KEY") 
                                )
    print(result_info)
```


#### 3. Configure Paths
You can configure the default paths for different languages in [opencoderunner/infos/run_info.py](opencoderunner/infos/run_info.py). For example, python path, cmake path, java JDK path, node.js path, etc. 

#### 4. More Examples
More examples for various code languages are in [examples/](examples/). You can run them easily.

## TODO
- [x] Sandbox for permission control
- [x] Project structure visualization
- [x] Input/argparse/stdin 
- [ ] PyPi/Conda
- [x] API key
- [x] Code str running (simple running)
- [ ] OpenAI tools
- [ ] Langchain tools


## Supported Languages
- [x] Python
- [x] JavaScript
- [x] TypeScript
- [x] C (CMake)
- [x] C++ (CMake)
- [x] Java
- [x] Dafny
- [x] Bash
- ...


## Update
- [**2025-04-17**] Launch OpenCodeRunner


## Contributors
😊 We welcome passionate contributors! If you are interested, feel free to contact!

[![Contributors](https://contrib.rocks/image?repo=OpenCodeRunner/OpenCodeRunner)](https://github.com/OpenCodeRunner/OpenCodeRunner/graphs/contributors)

