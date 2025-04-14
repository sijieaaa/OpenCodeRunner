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
                "file_relpath": "file1.py",
                "file_content": """
def main1():
    print("Hello World")
    return 123
"""
            },
            {
                "file_relpath": "file2.py",
                "file_content": """
import file1
from file1 import main1
def main2(a:str,b=1):
    output = main1()
    output = f"{a}-{b}-{output}"
    return [output, 1]
if __name__ == "__main__":
    main2()
"""
            }
        ],
        "language": "python",
        "project_root_name": "zproj1", 
        "entry_file_relpath": "file2.py",
        "entry_func_name": "main2",
        "entry_func_args": ["abc"],
        "entry_func_kwargs": {}
    }

    process_result_dict = run(run_info)
