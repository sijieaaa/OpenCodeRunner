

import os
import subprocess
import sys
from opencoderunner.languages.result_info import ResultInfo


def run_javascript_run_info(run_info: dict):
    """
    Run the code according to `run_info`.
    """


    
    # Import the function from the temporary file
    # project_root_dir = run_info["project_root_dir"]
    project_root_dir = run_info.project_root_dir

    # Bash path
    # bash_path = run_info.get("bash_path", "bash") 
    bash_path = run_info.bash_path

    # Temporary username
    # user = run_info.get("user", None)
    user = run_info.user

    # Firejail
    # use_firejail = run_info.get("use_firejail", True)
    use_firejail = run_info.use_firejail


    # Run
    cwd_bak = os.getcwd()
    os.chdir(project_root_dir)
    print(sys.path)
    sys.path[0] = project_root_dir
    print(sys.path)
    os.chdir(project_root_dir)
    result_info = ResultInfo()
    node_path = run_info.node_path
    javascript_bash_command = ""
    javascript_bash_command += f"cd {project_root_dir}\n"
    entry_file_abspath = run_info.entry_file_abspath
    javascript_bash_command += f"\n{node_path} {entry_file_abspath}"

    

    command = ""
    if user is not None:
        command += f"sudo -u {user} "
    
    command += f"cd {project_root_dir}\n"
    if use_firejail:
        command += f"firejail --quiet "
        whitelist = []
        whitelist.append(project_root_dir)
        whitelist.append(run_info.session_dir)
        for item in whitelist:
            command += f"--whitelist={item} "
        command += f"""{bash_path} <<EOF
{javascript_bash_command}
EOF
"""
    else:
        command += f"""{bash_path} <<EOF
{javascript_bash_command}
EOF
"""
        
    run_info.command = command
    run_info.print_command()
    result_info.command = command
    process_subrun = subprocess.run(
        command,
        shell=True,
        capture_output=True,
    )
    print(process_subrun)

    result_info.returncode = process_subrun.returncode
    result_info.stdout = process_subrun.stdout
    result_info.stderr = process_subrun.stderr

    return result_info