

import os, shutil, sys, json
import dotenv
dotenv.load_dotenv()

def write_file_from_file_info(file_info: dict) -> None:
    file_relpath = file_info["file_relpath"]
    file_root_dir = file_info["file_root_dir"]
    file_content = file_info["file_content"]
    """
    The `file_content` will be written to `os.path.join(file_root_dir, file_relpath)`
    """

    file_abs_path = os.path.join(file_root_dir, file_relpath)

    file_dir = os.path.dirname(file_abs_path)
    os.makedirs(file_dir, exist_ok=True)

    with open(file_abs_path, 'w') as f:
        f.write(file_content)
    return 


if __name__ == '__main__':
    file_info = {
        "file_relpath": "{file_root_name}/...", 
        "file_root_dir": "", 
        "file_content": None,
    }


    file_info["file_relpath"] = "dir1/file.py"
    file_info["file_root_dir"] = "proj1/"
    file_info["file_content"] = "print(\"Hello World\")"

    write_file_from_file_info(file_info)