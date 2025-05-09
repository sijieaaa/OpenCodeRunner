from typing import Literal


import shutil
import os
import random
import string
import json
import os



from opencoderunner.languages.python.run import run_python_run_info
from opencoderunner.languages.bash.run import run_bash_run_info
from opencoderunner.languages.java.run import run_java_run_info
from opencoderunner.languages.typescript.run import run_typescript_run_info
from opencoderunner.languages.javascript.run import run_javascript_run_info
from opencoderunner.languages.dafny.run import run_dafny_run_info
from opencoderunner.languages.sql.run import run_sql_run_info

from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo


ext_map = {
    "python": "py", 
    "bash": "sh",
    "cpp": "cpp",
    "java": "java",
    "dafny": "dfy",
    "javascript": "js",
    "typescript": "ts",
    "sql": "sql",
}


def rm_makedirs(dir_path: str):
    """
    Force to remove a directory. And then create a clean one.
    """
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)



def run(
        run_info: RunInfo,
        is_run: bool = True,
    ):
    language = run_info.language
    language = language.lower().strip()
    if run_info.project_root_name is None:
        run_info.project_root_name = "project_tmp"
    project_root_name = run_info.project_root_name



    # Create a temporary directory for the session
    TMP_ROOT = run_info.tmp_root
    session_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    session_dir = os.path.join(TMP_ROOT, session_name)
    rm_makedirs(session_dir)
    run_info.session_dir = session_dir


    # Update the `project_root_dir` to include the session name. So the structure will be:
    # TMP_ROOT 
    #   |-session_name
    #      |-project_root_name
    project_root_dir = os.path.join(TMP_ROOT, session_name, project_root_name)
    run_info.project_root_dir = project_root_dir
    rm_makedirs(project_root_dir)


    # Include `entry_file_abspath`
    if run_info.entry_file_relpath is not None:
        run_info.entry_file_abspath = os.path.join(project_root_dir, run_info.entry_file_relpath)
    else:
        run_info.entry_file_abspath = None


    if run_info.code_str is not None:
        if run_info.entry_file_relpath is not None:
            run_info.entry_file_relpath = run_info.entry_file_relpath
        else:
            run_info.entry_file_relpath = f"__code_str__.{ext_map[language]}"
        run_info.file_infos = [
            FileInfo(
                file_relpath=run_info.entry_file_relpath,
                file_content=run_info.code_str,
            )
        ]
        run_info.entry_file_relpath = run_info.file_infos[0].file_relpath
        run_info.entry_file_abspath = os.path.join(project_root_dir, run_info.entry_file_relpath)


    # Include `file_abspath`
    # Write all files in the run_info to temporary files
    for i in range(len(run_info.file_infos)):
        file_abspath = os.path.join(project_root_dir, run_info.file_infos[i].file_relpath)
        if not os.path.exists(os.path.dirname(file_abspath)):
            os.makedirs(os.path.dirname(file_abspath), exist_ok=True)
        run_info.file_infos[i].file_abspath = file_abspath
        file_content = run_info.file_infos[i].file_content
        with open(file_abspath, 'w') as f:
            f.write(file_content)
 



    if language in ["python", "py"]:
        result_info = run_python_run_info(run_info=run_info)
    elif language in ["bash"]:
        result_info = run_bash_run_info(run_info=run_info)
    elif language in ["java", "javac"]:
        result_info = run_java_run_info(run_info=run_info)
    elif language in ["typescript", "ts"]:
        result_info = run_typescript_run_info(run_info=run_info)
    elif language in ["javascript", "js"]:
        result_info = run_javascript_run_info(run_info=run_info)
    elif language in ["dafny", "dfy"]:
        result_info = run_dafny_run_info(run_info=run_info)
    elif language in ["sql"]:
        result_info = run_sql_run_info(run_info=run_info)
    else:
        raise NotImplementedError
    
    # Clean up the temporary directory
    if run_info.delete_after_run:
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)
    # print(result_info)


    return result_info


