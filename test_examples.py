import spacy

nlp = spacy.load('en')
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def get_cosine_sim(*strs): 
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)
    
def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()

str1 = "AI is our friend and it has been friendly"
str2 = "AI and humans have always been friendly"
str3 = "suka blta"

def get_cossine_sim(str1,str2):
    """
    Cosine similarity calculates similarity by measuring the cosine of angle between two vectors
    """
    doc1 = nlp(str1)
    doc2 = nlp(str2)
    return doc1.similarity(doc2)

print(get_cossine_sim(str1,str2))
print(get_cosine_sim(str1,str2,str3))