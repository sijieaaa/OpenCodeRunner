import tempfile
import subprocess
import os
import dotenv
import shutil
from languages.process_result import ProcessResult

dotenv.load_dotenv()
TMP_ROOT = os.getenv("TMP_ROOT")



def run_cpp_codestr(codestr: str):
    process_result = ProcessResult()

    with tempfile.TemporaryDirectory(dir=TMP_ROOT) as tmp_dir:
        cpp_path = os.path.join(tmp_dir, "main.cpp")
        exe_path = os.path.join(tmp_dir, "main.out")

        # Write in temporary C++ source file
        with open(cpp_path, "w") as f:
            f.write(codestr)

        # Compile to executable
        compile_process = subprocess.run(
            ["g++", cpp_path, "-o", exe_path],
            capture_output=True,
            text=True,
        )

        process_result.compile_returncode = compile_process.returncode
        process_result.compile_stdout = compile_process.stdout
        process_result.compile_stderr = compile_process.stderr

        if compile_process.returncode != 0:
            return process_result

        # Run the executable
        run_process = subprocess.run(
            [exe_path],
            capture_output=True,
            text=True,
        )
        process_result.returncode = run_process.returncode
        process_result.stdout = run_process.stdout
        process_result.stderr = run_process.stderr

    return process_result
    




if __name__ == '__main__':
    cpp_code = """
#include <iostream>
int main() {
    std::cout << "Hello from C++!" << std::endl;
    return 0;
}
"""

    process_result = run_cpp_codestr(cpp_code)

    print(process_result)

