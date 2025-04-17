

import time
import tqdm
from opencoderunner.run_on_server import run_with_bytes, run_with_msgpack
from opencoderunner.infos.run_info import RunInfo
from opencoderunner.infos.result_info import ResultInfo
from opencoderunner.infos.file_info import FileInfo

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

    t0 = time.time()
    for i in tqdm.tqdm(range(10)):
        result_info = run_with_msgpack(run_info=run_info, host=host, port=port)
    t1 = time.time()


    for i in tqdm.tqdm(range(10)):
        result_info = run_with_bytes(run_info=run_info, host=host, port=port)
    t2 = time.time()
    
    print(f"msgpack time: {t1 - t0}")
    print(f"bytes time: {t2 - t1}")