




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo



if __name__ == "__main__":


    run_info = RunInfo(
        code_str="""
class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
""",
        language="java",
        project_root_name="project_java",
        java_path="/home/runner/Tools/jdk-21/bin/java",
        javac_path="/home/runner/Tools/jdk-21/bin/javac",
    )
    run_info.print_tree()




    result_info = run_on_local(run_info=run_info)
    print(result_info)
    print(result_info.stdout)
    print(result_info.stdout.decode())
    a=1