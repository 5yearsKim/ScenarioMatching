from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

# Two lists of sentences
sentences1 = ['I am sleepy',
             'what is the price?',
             'The new movie is awesome',
             'I like you',
             ]

sentences2 = ['I\'m so tired now',
              'how much is it?',
              'The new movie is so great',
              'You like I',
             ]
import time
start = time.time()
#Compute embedding for both lists
embeddings1 = model.encode(sentences1, convert_to_tensor=True)
embeddings2 = model.encode(sentences2, convert_to_tensor=True)
print(embeddings1)
end = time.time()

print(end -start, 'time')

#Compute cosine-similarits
cosine_scores = util.cos_sim(embeddings1, embeddings2)

#Output the pairs with their score
for i in range(len(sentences1)):
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))
