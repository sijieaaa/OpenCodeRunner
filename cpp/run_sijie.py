import tempfile
import subprocess
import os
import dotenv
import shutil

dotenv.load_dotenv()
TMP_ROOT = os.getenv("TMP_ROOT")


class ProcessResult:
    def __init__(self):
        self.returncode = 0
        self.stdout = ""
        self.stderr = ""
        self.func_return = None
        self.compile_returncode = 0
        self.compile_stdout = ""
        self.compile_stderr = ""

    def __repr__(self):
        return (
            "====== ProcessResult ======\n"
            f"returncode: {self.returncode}\n"
            f"stdout: {self.stdout}\n"
            f"stderr: {self.stderr}\n"
            f"func_return: {self.func_return}\n"
            f"compile_returncode: {self.compile_returncode}\n"
            f"compile_stdout: {self.compile_stdout}\n"
            f"compile_stderr: {self.compile_stderr}\n"
            "===========================\n"
        )

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

