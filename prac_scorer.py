# from myscript.scorer import Scorer

# scorer = Scorer(load_path='ckpts/mtbert93.pt')
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
lemmatizer = nltk.stem.WordNetLemmatizer()

sentences1 = ['I was a big man',
             'what is the price?',
             'The new movie is awesome',
             'I don\'t eat apple',
             'I likes school',
             ]

def lemmantize_sentence(sent):
    words = sent.split()
    words = list(map(lambda w: lemmatizer.lemmatize(w), words))
    return ' '.join(words)

for sent in sentences1:
    print(lemmantize_sentence(sent))


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

# score, categories = scorer.score_sentence(sentences1, sentences2)
# print(score, categories)