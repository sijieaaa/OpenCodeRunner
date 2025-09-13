
from opencoderunner import RunInfo
from opencoderunner import run as opencr_run 

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="""
# oom_test.py
import resource
import time
import random
# a
soft, hard = resource.getrlimit(resource.RLIMIT_AS)
print(f"虚拟内存限制（bytes）: soft={soft}, hard={hard}")
for i in range(1000000):
    abc = random.randint(1, 1000000) * random.randint(1, 1000000) * random.randint(1, 1000000)

data = []
for i in range(10):
    data.append("x" * 1_000_000_000)  
    print(f"{(i+1)*1}GB allocated")
    time.sleep(1)


""",
        language="python",
        project_root_name="project_root_name",  
        session_name="session",  
        timeout=1, # Test timeout
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

