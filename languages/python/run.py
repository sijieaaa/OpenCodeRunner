import tempfile
import subprocess
import textwrap

import importlib.util
import os
from contextlib import redirect_stdout
import io
import dotenv
import sys
from deprecated import deprecated

from languages.file import write_file_from_file_info
from languages.process_result import ProcessResult


dotenv.load_dotenv()
TMP_ROOT = os.getenv("TMP_ROOT")



@deprecated
def find_python_interpreter(python_version, torch_version):
    conda_env_name = f"python{python_version}-torch{torch_version}"
    python_path = f"/home/runner/miniconda3/envs/{conda_env_name}" 
    return python_path




@deprecated
def run_python_codestr(codestr):
    process = subprocess.run(
        ["python", "-c", codestr],
        capture_output=True,
    )
    return process



@deprecated
def run_python_funcstr(funcstr: str, 
                       func_name: str = None,
                       func_args: dict = None,
                       ):
    # Write in a temporary file
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', dir=TMP_ROOT, delete=False) as f:
        f.write(funcstr)
        f.flush()
        filepath = f.name
    
    # Import the function from the temporary file
    func = import_function_from_file(filepath, func_name)
    
    # Call the function
    process_result = ProcessResult()
    try:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            func_return = func(**func_args)
        stdout = buffer.getvalue()
        process_result.func_return = func_return
        process_result.stdout = stdout
    except Exception as e:
        process_result.returncode = 1
        process_result.stderr = str(e)
        process_result.func_return = None
    os.remove(filepath)

    return process_result



def import_function_from_file(file_path, func_name):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, func_name)
    return func



def run_python_run_info(run_info: dict):
    """
    Run the Python code according to `run_info`.
    """
    # Write all files in the run_info to temporary files
    file_infos = run_info["file_infos"]
    for file_info in file_infos:
        write_file_from_file_info(file_info)

    # Run the entry function
    entry_func_name = run_info["entry_func_name"]
    entry_func_args = run_info["entry_func_args"]
    entry_func_kwargs = run_info["entry_func_kwargs"]
    
    # Import the function from the temporary file
    filepath = os.path.join(run_info["root_dir"], run_info["entry_file_relpath"])
    file_abspath = os.path.abspath(filepath)
    root_absdir = os.path.abspath(run_info["root_dir"])

    # Call the function
    process_result = ProcessResult()
    if entry_func_name is not None:
        # Change cwd + add `root_absdir` to sys.path. Otherwise, the import will fail
        cwd_bak = os.getcwd()
        os.chdir(root_absdir)
        print(sys.path)
        sys.path[0] = root_absdir
        print(sys.path)
        try:
            func = import_function_from_file(file_abspath, entry_func_name)
            sys.path[0] = cwd_bak
            os.chdir(cwd_bak)
        except Exception as e:
            process_result.returncode = 1
            process_result.stdout = ""
            process_result.stderr = str(e)
            sys.path[0] = cwd_bak
            os.chdir(cwd_bak)
            return process_result

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            try:
                entry_func_return = func(*entry_func_args, **entry_func_kwargs)
            except Exception as e:
                process_result.returncode = 1
                process_result.stdout = ""
                process_result.stderr = str(e)
                return process_result
        stdout = buffer.getvalue()
        process_result.entry_func_return = entry_func_return
        process_result.stdout = stdout

    # If `entry_func_name` is None, run the file directly
    else:
        cwd_bak = os.getcwd()
        os.chdir(run_info["root_dir"])
        try:
            process = subprocess.run(
                ["python", run_info["entry_file_relpath"]],
                capture_output=True,
            )
            process_result.returncode = process.returncode
            process_result.stdout = process.stdout
            process_result.stderr = process.stderr
        except Exception as e:
            process_result.returncode = process.returncode
            process_result.stdout = process.stdout
            process_result.stderr = process.stderr


    return process_result

