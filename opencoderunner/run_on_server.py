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
    


    