




from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo


if __name__ == "__main__":
    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="CMakeLists.txt",
                file_content="""
cmake_minimum_required(VERSION 3.10)
project(MyProject C CXX)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

include_directories(${CMAKE_SOURCE_DIR}/include)

file(GLOB_RECURSE SOURCES
    ${CMAKE_SOURCE_DIR}/src/*.cpp
    ${CMAKE_SOURCE_DIR}/src/*.c
)

add_executable(my_app ${SOURCES})

"""
            ),
            FileInfo(
                file_relpath="include/utils.h",
                file_content="""
#ifndef UTILS_H
#define UTILS_H

int add(int a, int b);

#endif

"""
            ),
            FileInfo(
                file_relpath="include/c_tools.h",
                file_content="""
#ifndef C_TOOLS_H
#define C_TOOLS_H

int multiply(int a, int b);

#endif



"""
            ),
            FileInfo(
                file_relpath="src/main.cpp",
                file_content="""
#include <iostream>
#include "utils.h"

extern "C" {
#include "c_tools.h"
}

int main() {
    std::cout << "3 + 4 = " << add(3, 4) << std::endl;
    std::cout << "3 * 4 = " << multiply(3, 4) << std::endl;
    return 0;
}

"""
            ),
            FileInfo(
                file_relpath="src/utils.cpp",
                file_content="""
#include "utils.h"

int add(int a, int b) {
    return a + b;
}

"""
            ),
            FileInfo(
                file_relpath="src/c_tools.c",
                file_content="""
#include "c_tools.h"

int multiply(int a, int b) {
    return a * b;
}
"""
            ),
        ],
        # As there needs many bash-related commands to run cmake, we use `bash` as the language.
        language="bash", 
        project_root_name="MyCMakeProject",
        use_firejail=False,
        delete_after_run=False,
        bash_command="""
rm -rf build
mkdir build 
cd build
cmake ..
make
./bin/my_app
"""
    )
    run_info.print_tree()

    result_info = run_on_local(
        run_info=run_info,
    )
    run_info.print_command()
    print(result_info)