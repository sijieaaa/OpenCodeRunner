

import os
import subprocess
import sys
from opencoderunner.languages.process_result import ProcessResult


def run_bash_run_info(run_info: dict):
    """
    Run the Python code according to `run_info`.
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

    # Bash command
    bash_command = run_info.get("bash_command", None)

    # Temporary username
    username = run_info.get("username", "tmp_user")

    # Call the function
    process_result = ProcessResult()
    command = f"""
firejail --quiet --whitelist={project_root_dir} bash <<'EOF'
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