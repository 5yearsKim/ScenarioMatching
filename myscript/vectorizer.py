from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoModel, AutoTokenizer

class PseudoModel:
    def __init__(self):
        pass

    def encode(self, sentences, convert_to_tensor=True):
        return torch.randn((len(sentences), 10))

class Vectorizer:
    def __init__(self, model_type='SentenceTransformer'):
        self.model_type= model_type
        if type == 'SentenceTransformer':
            self.model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
        else:
            self.model = CustomModel(pretrained_path='ckpts/distil-v1') 
        # self.model = PseudoModel()

    def vectorize(self, sentences):
        vectors = self.model.encode(sentences, convert_to_tensor=True)
        return vectors

    def __call__(self, sentences):
        return self.vectorize(sentences)

class CustomModel:
    def __init__(self, pretrained_path='ckpts/disttil-v1'):
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_path)
        self.bert = AutoModel.from_pretrained(pretrained_path).eval()
    
    def encode(self, sentences, convert_to_tensor=True):
        inputs = self.tokenizer(sentences, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            bout = self.bert(**inputs)
        vector = bout.last_hidden_state[:,0, :]
        return vector