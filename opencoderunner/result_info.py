
from typing import Optional, Literal, Any
from pydantic import BaseModel, ConfigDict
from pydantic import model_validator
import os, shutil, sys


class ResultInfo(BaseModel):
    # model_config = ConfigDict(extra="allow")  # Allow adding extra fields after initialization.
    
    command: Optional[str] = None  # Command to run the code. Optional for bash. Required for all other languages.
    tree_str: Optional[str] = None  # Tree structure of the files and directories created during the run. Useful for debugging and understanding the file structure.
    datetime_start: Optional[str] = None  # Start time
    datetime_end: Optional[str] = None  # End time

    # Compilation result
    compile_returncode: Optional[Any] = None
    compile_stdout: Optional[Any] = ""
    compile_stderr: Optional[Any] = ""

    # Execution result
    # Nearly for all languages
    returncode: Optional[Any] = None
    stdout: Optional[Any] = ""
    stderr: Optional[Any] = ""
    stdout_str: Optional[str] = ""  # String version of stdout
    stderr_str: Optional[str] = ""  # String version of stderr
    stdout_stderr: Optional[str] = ""  

    # Function return value
    # Currently only for Python
    entry_func_name: Optional[str] = ""
    entry_func_return: Optional[Any] = None

    def __str__(self):
        return (
            "====== ResultInfo ======\n"
            f"datetime_start: {self.datetime_start}\n"
            f"datetime_end: {self.datetime_end}\n"
            f"command: {self.command}\n"
            f"compile_returncode: {self.compile_returncode}\n"
            f"compile_stdout: {self.compile_stdout}\n"
            f"compile_stderr: {self.compile_stderr}\n"
            f"returncode: {self.returncode}\n"
            f"stdout: {self.stdout}\n"
            f"stderr: {self.stderr}\n"
            f"entry_func_name: {self.entry_func_name}\n"
            f"entry_func_return: {self.entry_func_return}\n"
            "========================\n"
        )


if __name__ == '__main__':
    process_result = ResultInfo()
    print(process_result)
    print(process_result.model_dump_json())
    print(process_result.model_dump())

    a = b"123"
    print(type(a))