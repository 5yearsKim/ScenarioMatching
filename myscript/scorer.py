import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

CATEGORIES = ['contradiction', 'neutral', 'entailment']

class Scorer:
    def __init__(self, load_path = 'ckpts/mtbert.pt'):
        self.model = MultiTaskBert()
        self.model.load(load_path)
        self.tknzr = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    
    def score_sentence(self, sent1, sent2):
        assert len(sent1) == len(sent2)
        inputs = self.tknzr(sent1, sent2, return_tensors='pt', padding=True, max_length=256, truncation=True)
        sim_score, category_score = self.model(inputs)
        category_score = nn.functional.softmax(category_score, dim=1)
        categories = self.score_to_category(category_score)
        return sim_score.tolist(), categories 

    def score_to_category(self, category_score):
        max_return = torch.max(category_score, dim=1)
        max_val, max_arg = max_return.values.tolist(), max_return.indices.tolist()
        holder = []
        for score, idx in zip(max_val, max_arg):
            if score > 0.7:
                holder.append(CATEGORIES[idx]) 
            else:
                holder.append('-')
        return holder



class MultiTaskBert(nn.Module):
    def __init__(self, pretrained_path='distilbert-base-uncased'):
        super().__init__()
        self.bert = AutoModel.from_pretrained(pretrained_path)
        out_dim = self.bert.config.dim
        self.binary_head = torch.nn.Linear(out_dim, 1)
        self.category_head = torch.nn.Linear(out_dim, 3)

    def forward(self, inputs):
        bout = self.bert(**inputs)
        binary_out = self.binary_head(bout.last_hidden_state[:, 0, :]).view(-1)
        category_out = self.category_head(bout.last_hidden_state[:, 1, :])
        return torch.sigmoid(binary_out), category_out 

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path, map_location='cpu'))