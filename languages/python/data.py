


import io
from typing import Any
from PIL import Image
import numpy as np
import pickle
import base64
import json
import os, shutil, sys



def read_data_from_data_info(data_info: dict) -> object:
    data_base64 = data_info["data_base64"]
    data_orginal = convert_from_data_base64(data_base64)
    return data_orginal


def convert_to_data_bytes(data: Any) -> bytes:
    """data -> bytes"""
    data_pickle = pickle.dumps(data)
    return data_pickle


def convert_from_data_bytes(data: bytes) -> Any:
    """bytes -> data"""
    data_original = pickle.loads(data)
    return data_original


def convert_to_data_base64(data: Any) -> str:
    """data -> bytes -> base64"""
    data_pickle = pickle.dumps(data)
    data_base64 = base64.b64encode(data_pickle).decode('utf-8')
    return data_base64


def convert_from_data_base64(data_base64: str) -> Any:
    """base64 -> bytes -> data"""
    data_bytes = base64.b64decode(data_base64)
    data_original = pickle.loads(data_bytes)
    return data_original



def construct_data_info(data: Any) -> dict:
    """
    `data_info` stores all JSON serializable data
    """
    data_base64 = convert_to_data_base64(data)
    data_language = f"python@{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    data_info = {
        "data_base64": data_base64,
        "data_language": data_language,
        "data_type": f"{type(data).__module__}.{type(data).__name__}",
    }
    return data_info



if __name__ == '__main__':
    data_info = {
        "data_base64": None,
        "data_language": None,
        "data_type": None,
    }


    # # -- PIL.Image
    # from PIL import Image
    # imagepath = '/home/runner/Tools/coderunner/opencoderunner_v3_notext.png'
    # image = Image.open(imagepath)
    # image = np.array(image)
    # data_orginal = image
    # data_info = construct_data_info(data_orginal)
    # data_info_json = json.dumps(data_info)


    # # -- numpy.ndarray
    # data_orginal = np.array([[1, 2, 3], [4, 5, 6]])
    # data_info = construct_data_info(data_orginal)
    # data_info_json = json.dumps(data_info)
    # data_info = json.loads(data_info_json)


    # # -- pandas.DataFrame
    # import pandas as pd
    # data_orginal = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    # data_info = construct_data_info(data_orginal)
    # data_info_json = json.dumps(data_info)
    # data_info_R = json.loads(data_info_json)
    # assert data_info_R == data_info


    # -- matplotlib.pyplot
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig = plt.figure()
    plt.plot(x, y)
    plt.savefig('plot.png')
    plt.close(fig)
    data_orginal = fig
    data_info = construct_data_info(data_orginal)
    a=1
    data_info_json = json.dumps(data_info)
    data_info_R = json.loads(data_info_json)
    assert data_info_R == data_info
    data_R = read_data_from_data_info(data_info_R)