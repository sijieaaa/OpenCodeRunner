import requests
from opencoderunner.languages.info import RunInfo, FileInfo
from opencoderunner.languages.result_info import ResultInfo

def run(run_info: RunInfo,
        host: str = "localhost",
        port: int = 8000,
        ): 
    service_url = f"http://{host}:{port}/run"
    
    run_info_dict = run_info.model_dump()

    # Note: `json=` should be a dict, not a JSON string
    response = requests.post(service_url, json=run_info_dict) 
    response.raise_for_status()
    
    result_info = ResultInfo.model_validate(response.json())
    print(result_info)

    return result_info
    


if __name__ == "__main__":
    run_info = RunInfo(
        file_infos=[
            FileInfo(
                file_relpath="file1.py",
                file_content="""print("Hello World")"""
            ),
        ],
        language="python",
        project_root_name="zproj1",
        entry_file_relpath="file1.py",
        use_firejail=False,
    )

    result_info = run(
        run_info=run_info,
        host="localhost",
        port=8000,
    )