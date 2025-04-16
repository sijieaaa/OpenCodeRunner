

import os
import subprocess
import sys
from opencoderunner.languages.process_result import ProcessResult


def run_java_run_info(run_info: dict):
    """
    Run the Java code according to `run_info`.
    """
    # Write all files in the run_info to temporary files
    file_infos = run_info["file_infos"]
    for i in range(len(file_infos)):
        file_info = file_infos[i]
        file_abspath = file_info["file_abspath"]
        os.makedirs(os.path.dirname(file_abspath), exist_ok=True)
        with open(file_abspath, 'w') as f:
            f.write(file_info["file_content"])
        assert os.path.exists(file_abspath)




    
    # Import the function from the temporary file
    project_root_dir = run_info["project_root_dir"]

    # Bash path
    bash_path = run_info.get("bash_path", "bash") 

    # Temporary username
    user = run_info.get("user", None)

    # Firejail
    use_firejail = run_info.get("use_firejail", True)



    # Run
    process_result = ProcessResult()
    java_path = run_info.get("java_path", "java")
    javac_path = run_info.get("javac_path", "javac")
    java_bash_command = ""
    java_bash_command += f"cd {project_root_dir}\n"
    java_bash_command += f"{javac_path} "
    for file_info in file_infos:
        file_abspath = file_info["file_abspath"]
        java_bash_command += f"{file_abspath} "
    entry_file_abspath = run_info.get("entry_file_abspath")
    java_bash_command += f"\n{java_path} {entry_file_abspath}"
    

    command = ""
    if user is not None:
        command += f"sudo -u {user} "
    
    if use_firejail:
        command += f"""firejail --quiet --whitelist={project_root_dir} {bash_path} <<'EOF'
{java_bash_command}
EOF
"""
    else:
        # TODO: EOF  'EOF'
        command += f"""bash <<EOF
{java_bash_command}
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