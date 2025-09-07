
from opencoderunner import RunInfo
from opencoderunner import run as opencr_run 

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="""
print('Hello World123')
import time
time.sleep(2)
print('Hello World')
""",
        language="python",
        project_root_name="project_root_name",  
        timeout=3, # Test timeout
    )                    

    # # -- Run locally
    for i in range(3):
        result_info = opencr_run(run_info=run_info)
        print(run_info.command)
        print(result_info)

