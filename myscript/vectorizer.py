from sentence_transformers import SentenceTransformer
import torch

class PseudoModel:
    def __init__(self):
        pass

    def encode(self, sentences, convert_to_tensor=True):
        return torch.randn((len(sentences), 10))

class Vectorizer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # self.model = PseudoModel()

    def vectorize(self, sentences):
        vectors = self.model.encode(sentences, convert_to_tensor=True)
        return vectors

    def __call__(self, sentences):
        return self.vectorize(sentences)