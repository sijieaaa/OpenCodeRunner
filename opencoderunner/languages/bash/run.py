

import os
import subprocess
import sys
from opencoderunner.languages.result_info import ResultInfo
from opencoderunner.languages.info import RunInfo, FileInfo

def run_bash_run_info(run_info: RunInfo):
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
    print(sys.path)
    sys.path[0] = project_root_dir
    print(sys.path)
    os.chdir(project_root_dir)
    process_result = ResultInfo()
    bash_command = run_info.bash_command
    command = ""
    if user is not None:
        command += f"sudo -u {user} "
    
    if use_firejail:
        command += f"firejail --quiet "
        whitelist = []
        whitelist.append(project_root_dir)
        for item in whitelist:
            command += f"--whitelist={item} "
        command += f"""{bash_path} <<EOF
{bash_command}
EOF
"""
    else:
        command += f"""{bash_path} <<EOF
{bash_command}
EOF
"""
    print(command)
    process_subrun = subprocess.run(
        command,
        shell=True,
        capture_output=True,
    )
    print(process_subrun)

    process_result.returncode = process_subrun.returncode
    process_result.stdout = process_subrun.stdout
    process_result.stderr = process_subrun.stderr

    return process_result