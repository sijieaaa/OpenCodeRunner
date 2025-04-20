




import os
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo



if __name__ == "__main__":



    run_info = {
        "file_infos": [
            {
                "file_relpath": "utils/MathUtils.dfy", # i.e. f"{project_root_name}/file1.py"
                "file_content": """
module utils.MathUtils {
    method Square(x: int) returns (y: int)
        ensures y == x * x
    {
        y := x * x;
    }

    function double(x: int): int
        ensures double(x) == x + x
    {
        x + x
    }
}

"""
            },
            {
                "file_relpath": "Main.dfy", # i.e. f"{project_root_name}/file2.py"
                "file_content": """
import opened utils.MathUtils

method Main() {
    print "Running Main...";
    var r := Square(3);
    print "Square(3) = ", r;
    print "double(4) = ", double(4);
}
"""
            }
        ],
        "language": "dafny",
        "project_root_name": "project_dafny", 
        "entry_file_relpath": "Main.dfy",
        
        
        # -- (Optional) Specify the java/javac path
        "dafny_path": "/home/runner/Tools/dafny/dafny", 

        # -- (Optional) Whether to use Firejail sandbox.
        "use_firejail": True, # bool
    }



    run_info = RunInfo(
        file_infos=[
            FileInfo(file_relpath="utils/MathUtils.dfy", 
                     file_content="""
module utils.MathUtils {
    method Square(x: int) returns (y: int)
        ensures y == x * x
    {
        y := x * x;
    }

    function double(x: int): int
        ensures double(x) == x + x
    {
        x + x
    }
}
"""
),
            FileInfo(file_relpath="Main.dfy", 
                     file_content="""
import opened utils.MathUtils

method Main() {
    print "Running Main...";
    var r := Square(3);
    print "Square(3) = ", r;
    print "double(4) = ", double(4);
}   
"""
),
        ],
        language="dafny",
        project_root_name="project_dafny",
        entry_file_relpath="Main.dfy",
        dafny_path="/home/runner/Tools/dafny/dafny",  # -- (Optional) Specify the java/javac path
    )
    
    

    result_info = run_on_local(run_info=run_info)
    print(result_info.stdout)
    print(result_info.stdout.decode())
    a=1