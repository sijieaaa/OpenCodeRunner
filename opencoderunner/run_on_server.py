import requests

from opencoderunner.run_info import RunInfo
from opencoderunner.result_info import ResultInfo
from opencoderunner.file_info import FileInfo

import pickle
import msgpack
import tqdm
import time
from typing import Optional, Literal
import dotenv

def run_with_bytes(run_info: RunInfo,
              host: str = "localhost",
              port: int = 8000,
              api_key: Optional[str] = None,
              ) -> ResultInfo: 
    service_url = f"http://{host}:{port}/run_bytes"
    run_info_bytes = pickle.dumps(run_info)
    response = requests.post(
        service_url,
        data=run_info_bytes,
        headers={
            "Content-Type": "application/octet-stream",
            "api_key": api_key,
        },
    )
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return response
    result_info: ResultInfo = pickle.loads(response.content)
    # print(result_info)
    return result_info



def run_with_msgpack(run_info: RunInfo,
                     host: str = "localhost",
                     port: int = 8000,
                     api_key: Optional[str] = None,
                     ) -> ResultInfo:
    service_url = f"http://{host}:{port}/run_msgpack"

    run_info_dict = run_info.model_dump()
    run_info_bytes = msgpack.packb(run_info_dict, use_bin_type=True)

    response = requests.post(
        service_url,
        data=run_info_bytes,
        headers={
            "Content-Type": "application/msgpack",
            "api_key": api_key, 
        },
    )
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return response

    result_dict = msgpack.unpackb(response.content, raw=False)
    result_info = ResultInfo.model_validate(result_dict)
    # print(result_info)
    return result_info




def run(
        run_info: RunInfo,
        host: str = "localhost",
        port: int = 8000,
        api_key: Optional[str] = None,
        mode: Literal["bytes", "msgpack"] = "msgpack",
) -> ResultInfo:
    """
    Run the code according to `run_info`.
    """
    if mode == "bytes":
        result_info = run_with_bytes(run_info=run_info, host=host, port=port, api_key=api_key)
    elif mode == "msgpack":
        result_info = run_with_msgpack(run_info=run_info, host=host, port=port, api_key=api_key)
    else:
        raise NotImplementedError
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
        use_firejail=True,
    )

    host = "0.0.0.0"
    port = 8000
    api_key = dotenv.get_key(".env", "OPENCODERUNNER_API_KEY")
    # api_key = '1'

    t0 = time.time()
    for i in tqdm.tqdm(range(10)):
        result_info = run_with_msgpack(run_info=run_info, host=host, port=port, api_key=api_key)
    t1 = time.time()


    for i in tqdm.tqdm(range(10)):
        result_info = run_with_bytes(run_info=run_info, host=host, port=port, api_key=api_key)
    t2 = time.time()
    
    print(f"msgpack time: {t1 - t0}")
    print(f"bytes time: {t2 - t1}")