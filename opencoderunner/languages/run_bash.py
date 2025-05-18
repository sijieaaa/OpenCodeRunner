

import os
import subprocess
import sys
from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.file_info import FileInfo

def run_bash_run_info(
        run_info: RunInfo, 
        is_run: bool = True
    ):
    """
    Run the code according to `run_info`.
    """

    project_root_dir = run_info.project_root_dir

    # Bash path
    bash_path = run_info.bash_path


    # Temporary username
    user = run_info.user

    # Firejail
    use_firejail = run_info.use_firejail


    # Run
    cwd_bak = os.getcwd()
    os.chdir(project_root_dir)
    # print(sys.path)
    sys.path[0] = project_root_dir
    # print(sys.path)
    os.chdir(project_root_dir)
    result_info = ResultInfo()




    bash_command = ""
    # bash_command += f"cd {project_root_dir}\n"
    if run_info.input_content is not None:
        bash_command += f"printf {repr(run_info.input_content)} | "
    bash_command += f"{bash_path} {run_info.entry_file_abspath}"



            
    command = bash_command



    run_info.command = command
    run_info.print_command()
    result_info.command = command
    # If do not run, just fill run_info
    if not is_run:
        return run_info
    try:
        process_subrun = subprocess.run(
            command.split(),
            shell=False,
            capture_output=True,
            cwd=project_root_dir,
            timeout=run_info.timeout,
        )
    except Exception as e:
        process_subrun = subprocess.CompletedProcess(
            args=command,
            returncode=1,
            stdout="",
            stderr=str(e),
        )
    # print(process_subrun)

    result_info.returncode = process_subrun.returncode
    result_info.stdout = process_subrun.stdout
    result_info.stderr = process_subrun.stderr

    # Change cwd back
    sys.path[0] = cwd_bak
    os.chdir(cwd_bak)
    
    return result_info