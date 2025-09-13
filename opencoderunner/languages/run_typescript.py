

import os
import subprocess
import sys
from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.file_info import FileInfo


def run_typescript_run_info(
        run_info: RunInfo, 
        is_run: bool = True
    ):
    """
    Run the Java code according to `run_info`.
    """
    # Write all files in the run_info to temporary files
    # file_infos = run_info["file_infos"]
    # for i in range(len(file_infos)):
    #     file_info = file_infos[i]
    #     file_abspath = file_info["file_abspath"]
    #     os.makedirs(os.path.dirname(file_abspath), exist_ok=True)
    #     with open(file_abspath, 'w') as f:
    #         f.write(file_info["file_content"])
    #     assert os.path.exists(file_abspath)




    
    # Import the function from the temporary file
    project_root_dir = run_info.project_root_dir

    # Bash path
    # bash_path = run_info.get("bash_path", "bash") 
    bash_path = run_info.bash_path

    # Temporary username
    # user = run_info.get("user", None)
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
    ts_node_path = run_info.ts_node_path
    typescript_bash_command = ""
    # typescript_bash_command += f"cd {project_root_dir}\n"
    entry_file_abspath = run_info.entry_file_abspath
    typescript_bash_command += f"\n{ts_node_path} --compiler-options '{{\"module\":\"CommonJS\"}}' {entry_file_abspath}"

    


    command = typescript_bash_command


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