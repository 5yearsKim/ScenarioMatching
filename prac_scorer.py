# from myscript.scorer import Scorer

# scorer = Scorer(load_path='ckpts/mtbert93.pt')
from nltk import edit_distance

def score_rule( s1, s2):
    s1, s2 = s1.lower().split(), s2.lower().split()
    len_max = max(len(s1), len(s2))
    return 1. - edit_distance(s1, s2) / len_max

# Two lists of sentences
sentences1 = ['I was a big man',
             'what is the price?',
             'The new movie is awesome',
             'I don\'t eat apple',
             'I like school',
             ]

sentences2 = ['I was a big man in the past',
              'how much is it?',
              'The new movie is so great',
              'I eat apple',
              'I hate school',
             ]

for s1, s2 in zip(sentences1, sentences2):
    dist = score_rule(s1, s2)
    print(dist)
# score, categories = scorer.score_sentence(sentences1, sentences2)
# print(score, categories)