from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.run_on_server import run as run_on_server
from opencoderunner.infos.run_info import RunInfo

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="import sys; import time; time.sleep(2); print(sys.stdin.read())",
        language="python",
        project_root_name="zproj1",  
        input_content="INPUT1\nINPUT2\n",
        timeout=1, # Test timeout
    )           
    run_info.print_tree()               

    # -- Run locally
    result_info = run_on_local(run_info=run_info)
    print(result_info)

    # -- is_run=False
    run_info = run_on_local(
        run_info=run_info,
        is_run=False
    )
    print(run_info)

    # -- Or Run on server
    result_info = run_on_server(run_info=run_info,
                                host="0.0.0.0",
                                port=8000,
                                api_key="12345"
                                )
    print(result_info)