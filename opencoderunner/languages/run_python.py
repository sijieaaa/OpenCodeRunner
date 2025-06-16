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

from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.file_info import FileInfo
import signal
import time

# dotenv.load_dotenv()
# TMP_ROOT = os.getenv("TMP_ROOT")



def find_python_path(python_version, torch_version):
    conda_env_name = f"python{python_version}-torch{torch_version}"
    python_path = f"/home/runner/miniconda3/envs/{conda_env_name}" 
    return python_path




# def import_function_from_file(file_path, func_name):
#     module_name = os.path.splitext(os.path.basename(file_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, file_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#     func = getattr(module, func_name)
#     return func


def import_function_from_file(file_path, func_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # -- Support hierachical: e.g. 'Solution.my_func'
    obj = module
    for attr in func_path.split("."):
        obj = getattr(obj, attr)
    return obj



def run_python_run_info(
        run_info: RunInfo, 
        is_run: bool = True
    ):
    """
    Run the Python code according to `run_info`.
    """


    # Run the entry function
    entry_func_name = run_info.entry_func_name
    entry_func_args = run_info.entry_func_args
    entry_func_kwargs = run_info.entry_func_kwargs
    

    # Import the function from the temporary file
    entry_file_abspath = run_info.entry_file_abspath
    project_root_dir = run_info.project_root_dir
    

    # Set python path
    python_path = run_info.python_path
    bash_path = run_info.bash_path

    # Temporary username
    user = run_info.user

    # Firejail
    use_firejail = run_info.use_firejail


    # Call the function
    if entry_func_name is not None:
        result_info = ResultInfo()
        try:
            func = import_function_from_file(entry_file_abspath, entry_func_name)
        except Exception as e:
            raise NotImplementedError

        buffer_stdout = io.StringIO()
        buffer_stdin = io.StringIO(run_info.input_content or "")
        old_stdin = sys.stdin
        sys.stdin = buffer_stdin

        try:
            with redirect_stdout(buffer_stdout):
                try:
                    entry_func_return = func(*entry_func_args, **entry_func_kwargs)
                    result_info.returncode = 0
                    result_info.stdout = buffer_stdout.getvalue()
                    result_info.stderr = ""
                    result_info.stdout_stderr = "\n".join([result_info.stdout, result_info.stderr])
                    result_info.entry_func_name = entry_func_name
                    result_info.entry_func_return = entry_func_return
                except Exception as e:
                    result_info.returncode = 1
                    result_info.stdout = buffer_stdout.getvalue()
                    result_info.stderr = str(e)
                    result_info.stdout_stderr = "\n".join([result_info.stdout, result_info.stderr])
                    result_info.entry_func_name = entry_func_name
                    result_info.entry_func_return = None
        finally:
            sys.stdin = old_stdin  # ← 确保恢复 stdin



    # If `entry_func_name` is None, run the file directly
    elif entry_func_name is None:
        # cwd_bak = os.getcwd()
        if not os.path.exists(project_root_dir):
            try:
                max_tries = 3
                for _ in range(max_tries):
                    print(f"[Warning] The project root directory `{project_root_dir}` does not exist. Creating all files...")
                    for i in range(len(run_info.file_infos)):
                        # If it is None
                        if run_info.file_infos[i].file_abspath is None:
                            run_info.file_infos[i].file_abspath = os.path.join(run_info.project_root_dir, run_info.file_infos[i].file_relpath)
                        if not os.path.exists(os.path.dirname(run_info.file_infos[i].file_abspath)):
                            os.makedirs(os.path.dirname(run_info.file_infos[i].file_abspath), exist_ok=True)
                        with open(run_info.file_infos[i].file_abspath, 'w') as f:
                            f.write(run_info.file_infos[i].file_content)
                    if os.path.exists(project_root_dir):
                        break
                    time.sleep(1)
            except Exception as e:
                print(e)

        os.chdir(project_root_dir)

        # print(sys.path)
        sys.path[0] = project_root_dir
        # print(sys.path)
        result_info = ResultInfo()


        python_bash_command = ""
        # python_bash_command += f"cd {project_root_dir}\n"
        if run_info.input_content is not None:
            python_bash_command += f"printf {repr(run_info.input_content)} | "
        python_bash_command += f"{python_path} {entry_file_abspath}"



        command = python_bash_command
            
        run_info.command = command
        result_info.command = command
        # If do not run, just fill run_info
        if not is_run:
            return run_info


        # # -- subprocess.run
        # try:
        #     # use_shell = True
        #     process_sub = subprocess.run(
        #         command if run_info.use_shell else command.split(),
        #         cwd=project_root_dir,
        #         capture_output=True,
        #         shell=run_info.use_shell,
        #         timeout=run_info.timeout,
        #     )
        #     process_sub.kill()
        # except Exception as e:
        #     process_sub.kill()
        #     process_sub = subprocess.CompletedProcess(
        #         args=command,
        #         returncode=1,
        #         stdout="",
        #         stderr=str(e),
        #     )
        # result_info.returncode = process_sub.returncode
        # result_info.stdout = process_sub.stdout
        # result_info.stderr = process_sub.stderr



        # -- subprocess.Popen
        try:
            process_sub = None
            process_sub = subprocess.Popen(
                command if run_info.use_shell else command.split(),
                cwd=project_root_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=run_info.use_shell,
            )
            stdout, stderr = process_sub.communicate(timeout=run_info.timeout)
            result_info.returncode = process_sub.returncode
            result_info.stdout = stdout
            result_info.stderr = stderr
            if process_sub:
                process_sub.kill()
                process_sub.wait()
        except Exception as e:
            if process_sub:
                process_sub.kill()
                process_sub.wait()
            process_sub = subprocess.CompletedProcess(
                args=command,
                returncode=1,
                stdout="",
                stderr=str(e),
            )
            result_info.returncode = process_sub.returncode
            result_info.stdout = process_sub.stdout
            result_info.stderr = process_sub.stderr




        if isinstance(result_info.stdout, bytes):
            result_info.stdout_str = result_info.stdout.decode()
        elif isinstance(result_info.stdout, str):
            result_info.stdout_str = result_info.stdout
        else:
            raise NotImplementedError
        
        if isinstance(result_info.stderr, bytes):
            result_info.stderr_str = result_info.stderr.decode()
        elif isinstance(result_info.stderr, str):
            result_info.stderr_str = result_info.stderr
        else:
            raise NotImplementedError
        result_info.stdout_stderr = "\n".join([result_info.stdout_str, result_info.stderr_str])

        # # Change cwd back
        # sys.path[0] = cwd_bak
        # os.chdir(cwd_bak)

    return result_info

