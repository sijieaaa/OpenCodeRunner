
from opencoderunner import RunInfo
from opencoderunner import run as opencr_run 

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="sleep 3",
        language="bash",
        timeout=2, # Test timeout
        is_quick_run=True, # Test quick run
    )                    

    # # -- Run locally
    for i in range(3):
        result_info = opencr_run(run_info=run_info)
        print(run_info.command)
        print(result_info)

