

from opencoderunner.languages.result_info import ResultInfo
from languages.file import write_file_from_file_info


def run_cpp_run_info(run_info: dict) -> ResultInfo: 
    """
    Run C++ according to `run_info`
    """
    # Write all files in the run_info to temporary files
    file_infos = run_info["file_infos"]
    for file_info in file_infos:
        write_file_from_file_info(file_info)

    # TODO: Add support for c++
    # NOTE: Need to support `compiler` config
    #       Be careful about single quote `''` and double quote `""` in C/C++

    return 
