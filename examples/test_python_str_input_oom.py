
from opencoderunner import RunInfo
from opencoderunner import run as opencr_run 

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="""
# oom_test.py
import resource
import time

soft, hard = resource.getrlimit(resource.RLIMIT_AS)
print(f"虚拟内存限制（bytes）: soft={soft}, hard={hard}")

data = []
for i in range(10):
    data.append("x" * 100_000_000)  
    print(f"{(i+1)*10}MB allocated")
    time.sleep(0.5)

""",
        language="python",
        project_root_name="project_root_name",  
        session_name="session_name",  
        timeout=10, # Test timeout
        input_content="123\n",
        use_shell=True,
        delete_after_run=False,
        pre_command="unset DISPLAY; ",  
        ram_limit_gb=8,  # Set RAM limit to 8GB
    )                    

    # # -- Run locally
    for i in range(3):
        result_info = opencr_run(run_info=run_info)
        print(run_info.command)
        print(result_info)
        None

