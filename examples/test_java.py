




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo



if __name__ == "__main__":



    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="folder1/Helper.java",
                file_content="""
package folder1;
public class Helper {
    public static void sayHello(String name) {
        System.out.println("Hello, " + name + "!");
    }
}
"""
            ),
            FileInfo(
                file_relpath="MainApp.java",
                file_content="""
import folder1.Helper;
public class MainApp {
    public static void main(String[] args) {
        System.out.println("Starting MainApp...");
        Helper.sayHello("Java");
    }
}
"""
            )
        ],

        language="java",
        project_root_name="project_java",
        entry_file_relpath="MainApp.java",
        java_path="/home/runner/Tools/jdk-21/bin/java",
        javac_path="/home/runner/Tools/jdk-21/bin/javac",
    )
    run_info.print_tree()




    result_info = run_on_local(run_info=run_info)
    print(result_info)
    print(result_info.stdout)
    print(result_info.stdout.decode())
    a=1