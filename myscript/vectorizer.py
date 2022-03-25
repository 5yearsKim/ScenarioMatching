from sentence_transformers import SentenceTransformer
import torch

class PseudoModel:
    def __init__(self):
        pass

    def encode(self, sentences):
        return torch.zeros((len(sentences), 10))

class Vectorizer:
    def __init__(self):
        # self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.model = PseudoModel()

    def vectorize(self, sentences):
        vectors = self.model.encode(sentences)
        return vectors

    def __call__(self, sentences):
        return self.vectorize(sentences)