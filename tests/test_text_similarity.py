'''
@author: Antonin Duroy
'''

from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from text_similarity import *

###############################################################################
# JACCARD SIMILARITY
###############################################################################
documents = ["Wikipedia is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation",
             "wiki is a collaboratively edited, unilangual, pay Internet encyclopedia supported by the non-profit Wikimedia Foundation",
             "Internet encyclopedia supported by the non-profit Wikimedia Foundation Wikipedia is a collaboratively edited, multilingual, free"]

tokenized_docs = [set(list(ngrams(word_tokenize(doc, 'french'), 1))) for doc in documents]

print('=== JACCARD SIMILARITY BETWEEN ===')
print(documents[0]+'\n'+documents[1])
print(jaccard_similarity(tokenized_docs[0], tokenized_docs[1]))
print(documents[0]+'\n'+documents[2])
print(jaccard_similarity(tokenized_docs[0], tokenized_docs[2]))
print(documents[1]+'\n'+documents[2])
print(jaccard_similarity(tokenized_docs[1], tokenized_docs[2]))

###############################################################################
# JARO WINKLER SIMILARITY
###############################################################################
print('\n=== JARO-WINKLER SIMILARITY BETWEEN ===')
print(documents[0])
print(documents[1])
#print(jaro_winkler_similarity("DWAYNE", "DUANE", 1, 0.1))
print(jaro_winkler_similarity(documents[0].split(), documents[1].split(), 3, 0.1))

###############################################################################
# COSINE SIMILARITY
###############################################################################
print('\n=== COSINE SIMILARITY BETWEEN ===')
print("Julie loves me more than Linda loves me")
print("Jane likes me more than Julie loves me")
print(cosine_similarity("Julie loves me more than Linda loves me".split(),
                        "Jane likes me more than Julie loves me".split()))

###############################################################################
# HAMMING DISTANCE
###############################################################################
print('\n=== HAMMING DISTANCE BETWEEN ===')
print("karolin")
print("kerstin")
print(hamming_distance("karolin", "kerstin"))
print("1011101")
print("1001001")
print(hamming_distance("1011101", "1001001"))
print("2173896")
print("2233796")
print(hamming_distance("2173896", "2233796"))

###############################################################################
# LEVENSHTEIN DISTANCE
###############################################################################
print('\n=== LEVENSHTEIN DISTANCE BETWEEN ===')
print('dkjsqndksjqbdjkqs')
print('dksqndknsqkdjbsbdhagvdagz')
print(levenshtein_distance("dkjsqndksjqbdjkqs", "dksqndknsqkdjbsbdhagvdagz"))
print(levenshtein_similarity("dkjsqndksjqbdjkqs", "dksqndknsqkdjbsbdhagvdagz"))

###############################################################################
# MINKOWSKI DISTANCE
###############################################################################
print('\n=== MINKOWSKI DISTANCE BETWEEN ===')
s1 = 'tito'
s2 = 'tata'
print(s1)
print(s2)
print(minkowski_distance(s1, s2, 2))
s1 = 'this is my first sentence for this'
s2 = 'that is the second sentence for that'
print(s1)
print(s2)
print(minkowski_distance(word_tokenize(s1, 'french'),
                         word_tokenize(s2, 'french'),
                         2))

###############################################################################
# MANHATTAN DISTANCE
###############################################################################
print('\n=== MANHATTAN DISTANCE BETWEEN ===')
print(s1)
print(s2)
print(manhattan_distance(word_tokenize(s1, 'french'), word_tokenize(s2, 'french')))
###############################################################################
# EUCLIDEAN DISTANCE
###############################################################################
print('\n=== EUCLIDEAN DISTANCE BETWEEN ===')
print(s1)
print(s2)
print(euclidean_distance(word_tokenize(s1, 'french'), word_tokenize(s2, 'french')))