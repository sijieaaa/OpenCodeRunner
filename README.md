<div align="center">
  <img src="https://github.com/OpenCodeRunner/OpenCodeRunner/blob/main/assets/opencoderunner_v3_marginborder.png" alt="OpenCodeRunner Logo" width="200"/>
  <br>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/blob/main/LICENSE">
    <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
  <a href="https://www.python.org/">
    <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  </a>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/stargazers">
    <img alt="GitHub Stars" src="https://img.shields.io/github/stars/OpenCodeRunner/OpenCodeRunner?style=social">
  </a>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/issues">
    <img alt="GitHub Issues" src="https://img.shields.io/github/issues/OpenCodeRunner/OpenCodeRunner">
  </a>
  <a href="https://github.com/OpenCodeRunner/OpenCodeRunner/commits/main">
    <img alt="Last Commit" src="https://img.shields.io/github/last-commit/OpenCodeRunner/OpenCodeRunner">
  </a>
</div>


# OpenCodeRunner
A fully open-source, free, and safe code runner that runs project-level (multi-file) code on both local machines and remote servers. It supports languages including `Python` `JavaScript/TypeScript` `Java` `Dafny` `Bash` etc.

OpenCodeRunner can be used in many ways:
- LLM, agent, reasoning, RL
- Project-level code evaluation
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
pip install -r requirements.txt
pip install -e .

# Uninstall
pip uninstall opencoderunner 
bash ./uninstall.sh
```
2. (Optional) Install Firejail sandbox for safety control (https://github.com/netblue30/firejail)
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
- Run on local machines via `Python`.
- Run on remote servers via `FastAPI`. Of course, you can also use this to run on local machines.

#### 1. Run on Local Machines
You can easily use `run_on_local` to obtain the results. You need to specify `RunInfo` `FileInfo`.
```python
import opencoderunner
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.file_info import FileInfo
from opencoderunner.infos.result_info import ResultInfo

if __name__ == "__main__":
    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="file1.py",
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
import file1
from file1 import main1
def main2(a:str,b=1):
    output = main1()
    output = f"{a}-{b}-{output}"
    print(output)
    return output
if __name__ == "__main__":
    main2("abc", b=123)
"""
            )
        ],
        language="python",
        project_root_name="zproj1",
        entry_file_relpath="file2.py",
        use_firejail=True,
    )
    run_info.print_tree()
    process_result_dict = run_on_local(run_info=run_info)
    print(process_result_dict)
```

#### 2. Run on Remote Servers
To run on remote servers, firstly you need to start FastAPI on your remote servers using `uvicorn`. Make sure your remote server has also installed OpenCodeRunner.

```bash
# Under OpenCodeRunner's root dir. E.g., `/home/user/OpenCodeRunner/`
uvicorn opencoderunner.server:app --host 0.0.0.0 --port 8000 --reload
```

Then in the client, you need to specify `host` and `port` in `run_on_server` to run on remote servers

```python
import time
import opencoderunner
from opencoderunner.run_on_server import run as run_on_server
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo

if __name__ == "__main__":
    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="file1.py",
                file_content="""print("Hello World")"""
            ),
        ],
        language="python",
        project_root_name="zproj1",
        entry_file_relpath="file1.py",
        use_firejail=True,
    )

    host = "0.0.0.0"
    port = 8000

    result_info = run_on_server(
        run_info=run_info,
        host=host,
        port=port,
    )
```

#### 3. More Examples
You can check `examples/` for more usage examples.

## TODO
- [x] Sandbox for permission control
- [x] User
- [ ] Structural .env config
- [x] Project structure visualization
- [ ] Input/argparse/stdin 
- [ ] Input blocking issue


## Supported Languages
- [x] Python
- [x] JavaScript
- [x] TypeScript
- [ ] C
- [ ] C++
- [x] Java
- [x] Dafny
- [x] Bash
- ...


## Update
- [**2025-04-17**] Launch OpenCodeRunner


## Contributors
😊 We welcome passionate contributors! If you are interested, feel free to contact!

[![Contributors](https://contrib.rocks/image?repo=OpenCodeRunner/OpenCodeRunner)](https://github.com/OpenCodeRunner/OpenCodeRunner/graphs/contributors)

