import json
from types import SimpleNamespace
import numpy as np
import nltk

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

lemmatizer = nltk.stem.WordNetLemmatizer()
def lemmatize_sentence(sent):
    words = sent.split()
    words = list(map(lambda w: lemmatizer.lemmatize(w), words))
    return ' '.join(words)

def edit_score(s1, s2, n=1):
    s1, s2 = lemmatize_sentence(s1.lower()), lemmatize_sentence(s2.lower())
    len_max = max(len(s1), len(s2))
    score = 1. - nltk.edit_distance(s1, s2) / len_max
    score = pow(score, n)
    return score

if __name__ == "__main__":
    files_from = ['scenario/sample.json']