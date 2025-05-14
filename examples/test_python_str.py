
from opencoderunner.run_info import RunInfo
from opencoderunner import run 

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="import sys; print(sys.stdin.read())",
        language="python",
        project_root_name="project_root_name",  
        input_content="INPUT1\nINPUT2\n",
        timeout=1, # Test timeout
    )                    

    # # -- Run locally
    for i in range(3):
        result_info = run(run_info=run_info)
        print(run_info.command)
        print(result_info)

    # -- Or Run on server
    for i in range(3):
        result_info = run(run_info=run_info,
                        host="0.0.0.0",
                        port=8000,
                        api_key="12345"
                        )
        print(result_info)