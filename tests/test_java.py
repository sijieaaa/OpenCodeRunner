




import os
from opencoderunner.run_on_local import run as run_on_local



if __name__ == "__main__":



    run_info = {
        "file_infos": [
            {
                "file_relpath": "folder1/Helper.java", # i.e. f"{project_root_name}/file1.py"
                "file_content": """
package folder1;

public class Helper {
    public static void sayHello(String name) {
        System.out.println("Hello, " + name + "!");
    }
}
"""
            },
            {
                "file_relpath": "MainApp.java", # i.e. f"{project_root_name}/file2.py"
                "file_content": """
import folder1.Helper;

public class MainApp {
    public static void main(String[] args) {
        System.out.println("Starting MainApp...");
        Helper.sayHello("Java");
    }
}
"""
            }
        ],
        "language": "java",
        "project_root_name": "project_java", 
        "entry_file_relpath": "MainApp.java",
        
        # -- (Optional) Specify the java/javac path
        "java_path": "/home/runner/Tools/jdk-21/bin/java", 
        "javac_path": "/home/runner/Tools/jdk-21/bin/javac", 

        # -- (Optional) You can specify the user to run the code
        # "user": "runner", # str or None
        "user": None, # str or None

        # -- (Optional) Whether to use Firejail sandbox
        "use_firejail": False, # bool
    }

    process_result_dict = run_on_local(run_info=run_info)
    a=1