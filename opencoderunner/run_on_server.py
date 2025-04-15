import requests


def run(run_info: dict,
        ip: str = "localhost",
        port: int = 8000,
        ): 
    # `json=` should input a dict, not a json string
    service_url = f"http://{ip}:{port}/run"
    response = requests.post(service_url, 
                            json=run_info 
                            )
    process_result_dict = response.json()
    print(process_result_dict)
    return process_result_dict
    


if __name__ == "__main__":



    run_info = {
        "file_infos": [
            {
                "file_relpath": "file1.py", # i.e. f"{project_root_name}/file1.py"
                "file_content": """
def main1():
    print("Hello World")
    return 123
"""
            },
            {
                "file_relpath": "file2.py", # i.e. f"{project_root_name}/file2.py"
                "file_content": """
import file1
from file1 import main1
def main2(a:str,b=1):
    output = main1()
    output = f"{a}-{b}-{output}"
    return output
if __name__ == "__main__":
    main2()
"""
            }
        ],
        "language": "python",
        "project_root_name": "zproj1", 
        "entry_file_relpath": "file2.py",
        "entry_func_name": "main2", # [str, None/Literal["__main__"]]
        "entry_func_args": ["abc"], # list
        "entry_func_kwargs": {"b": 123}, # dict
    }
    process_result = run(
        run_info
    )           
    print(process_result)              

