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
import signal
from contextlib import contextmanager
from datetime import datetime, timezone
import resource
import traceback


def preexec_fn(ram_limit_gb, timeout):
    def _fn():
        try:
            os.setsid()
            ram_limit_bytes = int(ram_limit_gb * 1024**3)
            resource.setrlimit(resource.RLIMIT_AS, (ram_limit_bytes, ram_limit_bytes))
            resource.setrlimit(resource.RLIMIT_CPU, (int(timeout), int(timeout)))  # ! only raise "Killed\n" 
        except Exception:
            import sys, traceback
            print("[OpenCodeRunner] timed out or OOM preexec_fn setting exception:", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            sys.stderr.flush()
            os._exit(1)
    return _fn




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
        python_bash_command += run_info.pre_command
        # python_bash_command += f"cd {project_root_dir}\n" # non-shell not support cd
        if run_info.input_content is not None:
            python_bash_command += f"printf {repr(run_info.input_content)} | "
        # python_bash_command += f"prlimit --as={int(run_info.ram_limit_gb * 1024**3)} -- "  
        # if run_info.timeout > 0:
        #     python_bash_command += f"timeout {run_info.timeout}s "
        python_bash_command += f"{python_path} {entry_file_abspath}"
        # if run_info.timeout > 0:
        #     python_bash_command += f" || (>&2 echo '[OpenCodeRunner] timed out after {run_info.timeout} seconds or OOM {run_info.ram_limit_gb} GB')"


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
        process_sub = None
        datetime_start = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC%z")
        result_info.datetime_start = datetime_start
        try:
            process_sub = subprocess.Popen(
                command if run_info.use_shell else command.split(),
                cwd=project_root_dir,
                preexec_fn=preexec_fn(
                    ram_limit_gb=run_info.ram_limit_gb, 
                    timeout=run_info.timeout
                ),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=run_info.use_shell,
                executable="/bin/bash"
            )
            stdout, stderr = process_sub.communicate(timeout=run_info.timeout)
            result_info.returncode = process_sub.returncode
            if result_info.returncode > 128: # Killed by signal
                result_info.stdout = stdout
                result_info.stderr = f"[OpenCodeRunner] returncode {result_info.returncode} Killed timed out {run_info.timeout} seconds or OOM {run_info.ram_limit_gb} GB"
            else:
                result_info.stdout = stdout
                result_info.stderr = stderr
        except subprocess.TimeoutExpired:
            stdout = ""
            if process_sub and process_sub.poll() is None:
                try:
                    os.killpg(os.getpgid(process_sub.pid), signal.SIGKILL)
                except Exception as e:
                    print(f"[OpenCodeRunner] timed out to kill process group: {e}")
            if process_sub:
                stdout, _ = process_sub.communicate()
            result_info.stdout = stdout
            result_info.stderr = f"[OpenCodeRunner] timed out after {run_info.timeout} seconds"
        except Exception as e:
            stdout = ""
            if process_sub:
                stdout, _ = process_sub.communicate()
            result_info.returncode = 1
            result_info.stdout = stdout
            result_info.stderr = str(e)
        finally:
            datetime_end = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC%z")
            result_info.datetime_end = datetime_end
            # double-check: kill anything left
            if isinstance(process_sub, subprocess.Popen) and process_sub.poll() is None:
                try:
                    os.killpg(os.getpgid(process_sub.pid), signal.SIGTERM)
                except Exception as e:
                    print(f"[OpenCodeRunner] timed out or failed to kill process group: {e}")


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

