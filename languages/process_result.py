
class ProcessResult:
    def __init__(self):
        # Compilation result
        # E.g., `g++ -o hello hello.cpp`
        self.compile_returncode = 0
        self.compile_stdout = ""
        self.compile_stderr = ""

        # Execution result
        # Nearly for all languages
        self.returncode = 0
        self.stdout = ""
        self.stderr = ""

        # Function return value
        # Currently only for Python
        self.entry_func_name = ""
        self.entry_func_return = None

    def __repr__(self):
        return (
            "====== ProcessResult ======\n"
            f"compile_returncode: {self.compile_returncode}\n"
            f"compile_stdout: {self.compile_stdout}\n"
            f"compile_stderr: {self.compile_stderr}\n"
            f"returncode: {self.returncode}\n"
            f"stdout: {self.stdout}\n"
            f"stderr: {self.stderr}\n"
            f"entry_func_name: {self.entry_func_name}\n"
            f"entry_func_return: {self.entry_func_return}\n"
            "===========================\n"
        )
