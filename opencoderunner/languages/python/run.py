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

from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo

dotenv.load_dotenv()
TMP_ROOT = os.getenv("TMP_ROOT")



def find_python_path(python_version, torch_version):
    conda_env_name = f"python{python_version}-torch{torch_version}"
    python_path = f"/home/runner/miniconda3/envs/{conda_env_name}" 
    return python_path




def import_function_from_file(file_path, func_name):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, func_name)
    return func



def run_python_run_info(run_info: RunInfo):
    """
    Run the Python code according to `run_info`.
    """


    # Run the entry function
    entry_func_name = run_info.entry_func_name
    entry_func_args = run_info.entry_func_args
    entry_func_kwargs = run_info.entry_func_kwargs
    

    # Import the function from the temporary file
    entry_file_abspath = getattr(run_info, "entry_file_abspath", None)
    project_root_dir = run_info.project_root_dir
    

    # Set python path
    python_path = run_info.python_path
    bash_path = run_info.bash_path

    # Temporary username
    user = run_info.user

    # Firejail
    use_firejail = run_info.use_firejail


    # Call the function
    process_result = ResultInfo()
    if entry_func_name is not None:
        # TODO
        raise NotImplementedError
        # Change cwd + add `root_absdir` to sys.path. Otherwise, the import will fail
        cwd_bak = os.getcwd()
        os.chdir(project_root_dir)
        print(sys.path)
        sys.path[0] = project_root_dir
        print(sys.path)
        try:
            func = import_function_from_file(entry_file_abspath, entry_func_name)
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
    elif entry_func_name is None:
        cwd_bak = os.getcwd()
        os.chdir(project_root_dir)
        print(sys.path)
        sys.path[0] = project_root_dir
        print(sys.path)
        result_info = ResultInfo()


        # Code str running
        if run_info.code_str is not None:
            python_bash_command = ""
            python_bash_command += f"cd {project_root_dir}\n"
            python_bash_command += f"printf {repr(run_info.input_content)} | {python_path} -c {repr(run_info.code_str)}"
        # Project file running
        else:
            python_bash_command = ""
            python_bash_command += f"cd {project_root_dir}\n"
            python_bash_command += f"printf {repr(run_info.input_content)} | {python_path} {entry_file_abspath}"
            
        # whitelist = []
        # whitelist.append(project_root_dir)
        # whitelist.append(run_info.session_dir)
        # whitelist_command = ""
        # for item in whitelist:
        #     whitelist_command += f"--whitelist={item} "
    
        # if run_info.use_firejail:
        #     command = f"cd {project_root_dir} && firejail {whitelist_command} --quiet -- printf {repr(run_info.input_content)} | {python_path} {entry_file_abspath}"
        # else:
        #     command = f"cd {project_root_dir} && printf {repr(run_info.input_content)} {python_path} {entry_file_abspath}"

        command = python_bash_command
            
        run_info.command = command
        run_info.print_command()
        result_info.command = command
        process_subrun = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            cwd=project_root_dir,
        )
        print(process_subrun)

        result_info.returncode = process_subrun.returncode
        result_info.stdout = process_subrun.stdout
        result_info.stderr = process_subrun.stderr

        # Change cwd back
        sys.path[0] = cwd_bak
        os.chdir(cwd_bak)

    return result_info

