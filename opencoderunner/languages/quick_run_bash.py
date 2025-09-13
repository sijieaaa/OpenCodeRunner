

import os
import subprocess
import sys
from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.file_info import FileInfo
from datetime import datetime, timezone
import signal
import resource


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




def quick_run_bash_run_info(
        run_info: RunInfo, 
        is_run: bool = True
    ):
    """
    Run the code according to `run_info`.
    """




    result_info = ResultInfo()
    result_info.command = run_info.code_str
    command = run_info.code_str
    project_root_dir = run_info.project_root_dir





    # -- subprocess.Popen
    process_sub = None
    datetime_start = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC%z")
    result_info.datetime_start = datetime_start
    try:
        process_sub = subprocess.Popen(
            command,
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
                print(f"[OpenCodeRunner] timed out or OOM to kill process group: {e}")
        if process_sub:
            stdout, _ = process_sub.communicate()
        result_info.stdout = stdout
        result_info.stderr = f"[OpenCodeRunner] timed out or OOM after {run_info.timeout} seconds"
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

