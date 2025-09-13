from typing import Literal


import shutil
import os
import random
import string
import json
import os



from opencoderunner.languages.run_python import run_python_run_info
from opencoderunner.languages.run_bash import run_bash_run_info
from opencoderunner.languages.run_java import run_java_run_info
from opencoderunner.languages.run_typescript import run_typescript_run_info
from opencoderunner.languages.run_javascript import run_javascript_run_info
from opencoderunner.languages.run_dafny import run_dafny_run_info
from opencoderunner.languages.run_sql import run_sql_run_info

from opencoderunner.languages.quick_run_bash import quick_run_bash_run_info


from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.file_info import FileInfo


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



def build_tree_str(root_path, indent="", is_last=True, is_root=True):
    lines = []
    # root dir show as absolute path
    if is_root:
        display_name = os.path.abspath(root_path).rstrip("/") + "/"
        lines.append(display_name)
    else:
        basename = os.path.basename(root_path.rstrip("/")) or root_path
        if os.path.isdir(root_path):
            basename += "/"
        connector = "└── " if is_last else "├── "
        lines.append(indent + connector + basename)
        indent += "    " if is_last else "│   "

    if os.path.isdir(root_path):
        try:
            entries = sorted(os.listdir(root_path))
        except PermissionError:
            entries = []
        for i, entry in enumerate(entries):
            full_path = os.path.join(root_path, entry)
            is_last_entry = (i == len(entries) - 1)
            lines.append(build_tree_str(full_path, indent, is_last_entry, is_root=False))
    
    return "\n".join(lines)




def run(
        run_info: RunInfo,
        is_run: bool = True,
    ):
    language = run_info.language
    language = language.lower().strip()

 




    # Create session_dir
    if run_info.session_name is None:
        run_info.session_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    run_info.session_dir = os.path.join(run_info.tmp_root, run_info.session_name)
    rm_makedirs(run_info.session_dir)




    # Create project_root_dir
    # TMP_ROOT 
    #   |-session_name (can be random)
    #      |-project_root_name
    if run_info.project_root_name is None:
        run_info.project_root_name = "project_root_name"
    run_info.project_root_dir = os.path.join(run_info.tmp_root, run_info.session_name, run_info.project_root_name)
    rm_makedirs(run_info.project_root_dir)


    # Option - Quick run
    if run_info.is_quick_run:
        if language in ['bash']:
            result_info = quick_run_bash_run_info(run_info=run_info, is_run=is_run) 
        
        return result_info
            

    # Option - Not quick run
    if not run_info.is_quick_run:

        # Include `entry_file_abspath`
        if run_info.entry_file_relpath is not None:
            run_info.entry_file_abspath = os.path.join(run_info.project_root_dir, run_info.entry_file_relpath)
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
            run_info.entry_file_abspath = os.path.join(run_info.project_root_dir, run_info.entry_file_relpath)
            # Remve the code_str
            run_info.code_str = None


        # Include `file_abspath`
        # Write all files in the run_info to temporary files
        for i in range(len(run_info.file_infos)):
            # If it is None
            if run_info.file_infos[i].file_abspath is None:
                run_info.file_infos[i].file_abspath = os.path.join(run_info.project_root_dir, run_info.file_infos[i].file_relpath)
            if not os.path.exists(os.path.dirname(run_info.file_infos[i].file_abspath)):
                os.makedirs(os.path.dirname(run_info.file_infos[i].file_abspath), exist_ok=True)
            with open(run_info.file_infos[i].file_abspath, 'w') as f:
                f.write(run_info.file_infos[i].file_content)


        if language in ["python", "py"]:
            result_info = run_python_run_info(run_info=run_info, is_run=is_run)
        elif language in ["bash"]:
            result_info = run_bash_run_info(run_info=run_info, is_run=is_run)
        elif language in ["java", "javac"]:
            result_info = run_java_run_info(run_info=run_info, is_run=is_run)
        elif language in ["typescript", "ts"]:
            result_info = run_typescript_run_info(run_info=run_info, is_run=is_run)
        elif language in ["javascript", "js"]:
            result_info = run_javascript_run_info(run_info=run_info, is_run=is_run)
        elif language in ["dafny", "dfy"]:
            result_info = run_dafny_run_info(run_info=run_info, is_run=is_run)
        elif language in ["sql"]:
            result_info = run_sql_run_info(run_info=run_info, is_run=is_run)
        else:
            raise NotImplementedError
        

        # Add tree structure to the result_info
        tree_str = build_tree_str(run_info.project_root_dir)
        result_info.tree_str = tree_str
    


    # Clean up the temporary directory
    if run_info.delete_after_run:
        max_attempts = 2
        for i in range(max_attempts):
            if os.path.exists(run_info.session_dir):
                try:
                    shutil.rmtree(run_info.session_dir)
                except Exception as e:
                    print(f"[Warning] Failed to delete {run_info.session_dir}: {e}")



    return result_info


