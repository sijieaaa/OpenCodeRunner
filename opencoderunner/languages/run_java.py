

import os
import subprocess
import sys
from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.file_info import FileInfo


def run_java_run_info(
        run_info: RunInfo, 
        is_run: bool = True
    ):
    """
    Run the code according to `run_info`.
    """


    
    # Import the function from the temporary file
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
    result_info = ResultInfo()
    java_path = run_info.java_path
    javac_path = run_info.javac_path
    java_bash_command = ""
    # java_bash_command += f"cd {project_root_dir}\n"
    java_bash_command += f"{javac_path} "
    for file_info in run_info.file_infos:
        file_abspath = file_info.file_abspath
        java_bash_command += f"{file_abspath} "
    java_bash_command += "\n"
    if run_info.input_content is not None:
        java_bash_command += f"printf {repr(run_info.input_content)} | "
    java_bash_command += f"{java_path} {run_info.entry_file_abspath}"
    

#     command = ""
#     if user is not None:
#         command += f"sudo -u {user} "
    
#     command += f"cd {project_root_dir}\n"
#     if use_firejail:
#         command += f"firejail --quiet "
#         whitelist = []
#         whitelist.append(project_root_dir)
#         whitelist.append(run_info.session_dir)
#         # whitelist.append(java_path)
#         # whitelist.append(javac_path)
#         for item in whitelist:
#             command += f"--whitelist={item} "
#         command += f"""{bash_path} <<EOF
# {java_bash_command}
# EOF
# """
#     else:
#         command += f"""{bash_path} <<EOF
# {java_bash_command}
# EOF
# """
        
    # whitelist = []
    # whitelist.append(project_root_dir)
    # whitelist.append(run_info.session_dir)
    # whitelist_command = ""
    # for item in whitelist:
    #     whitelist_command += f"--whitelist={item} "
    
    
    # if run_info.use_firejail:
    #     command = f"cd {project_root_dir} && firejail {whitelist_command} --quiet -- {bash_path} <<EOF\n{java_bash_command}\nEOF"
    # else:
    #     command = f"cd {project_root_dir} && {bash_path} <<EOF\n{java_bash_command}\nEOF"

    command = java_bash_command
            

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
            executable="/bin/bash"
        )
    except Exception as e:
        process_subrun = subprocess.CompletedProcess(
            args=command,
            returncode=1,
            stdout="",
            stderr=str(e),
        )
    print(process_subrun)

    result_info.returncode = process_subrun.returncode
    result_info.stdout = process_subrun.stdout
    result_info.stderr = process_subrun.stderr

    # Change cwd back
    sys.path[0] = cwd_bak
    os.chdir(cwd_bak)
    
    return result_info