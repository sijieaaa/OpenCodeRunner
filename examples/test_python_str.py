
import dotenv
from opencoderunner.run_on_local import run as run_on_local
from opencoderunner.run_on_server import run as run_on_server
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo

if __name__ == "__main__":
    run_info = RunInfo(
        code_str="import sys; print(sys.stdin.read())",
        language="python",
        project_root_name="zproj1",  
        input_content="INPUT1\nINPUT2\n",
    )           
    run_info.print_tree()               

    # -- Run locally
    result_info = run_on_local(run_info=run_info)
    print(result_info)

    # -- Or Run on server
    result_info = run_on_server(run_info=run_info,
                                host="0.0.0.0",
                                port=8000,
                                api_key="sample-api-key-1",
                                # You can set Server/Client API keys in `.env`
                                # api_key=dotenv.get_key(".env", "OPENCODERUNNER_API_KEY") 
                                )
    print(result_info)