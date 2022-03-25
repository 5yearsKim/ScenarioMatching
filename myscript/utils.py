import json
from types import SimpleNamespace
import numpy as np

def read_scenario(scenario_file):
    with open(scenario_file, 'r') as fr:
        scenario = json.load(fr, object_hook=lambda d: SimpleNamespace(**d))
        return scenario

def batching_list(my_list, n=4):
    final = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )] 
    return final


def np_to_blob(data):
    data = data.astype(np.float32)
    blob = data.tobytes()
    return blob 

def blob_to_np(blob):
    element = np.frombuffer(blob, dtype=np.float32)
    return element


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6) 

        
if __name__ == "__main__":
    files_from = ['scenario/sample.json']