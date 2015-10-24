'''
@author: Antonin Duroy
'''

import numpy as np

from math import floor
from scipy.spatial.distance import cosine
from nltk.probability import FreqDist

###############################################################################
# JACCARD SIMILARITY
###############################################################################
def jaccard_similarity(seq1, seq2):
    """ 1 means that seq1 and seq2 are equal
    0 means that seq1 and seq2 are completely different
    """
    set1 = set(seq1)
    set2 = set(seq2)
    u = set1.union(set2)
    i = set1.intersection(set2)
    return len(i)/len(u)

###############################################################################
# JARO WINKLER SIMILARITY
###############################################################################
def areEqual(seq1, index1, seq2, index2):
    try:
        return seq1[index1] == seq2[index2]
    except IndexError:
        return False

def normalizeWindow(start, end, max_limit, min_limit=0):
    if start < min_limit:
        start = min_limit
    if end > max_limit:
        end = max_limit
    return range(start, end)

def jaro_winkler_similarity(seq1, seq2, prefix_len=3, coef=0.1):
    """ 1 means that seq1 and seq2 are equal
    0 means that seq1 and seq2 are completely different
    """
    size1 = len(seq1)
    size2 = len(seq2)
    window = floor(max(size1, size2)/2) - 1
    
    matching_tokens = []
    transpositions = []
    for i, token1 in enumerate(seq1):
        for j, token2 in enumerate(seq2):
            if j in normalizeWindow(i-window, i+window, max(size1, size2)) and token1 == token2:
                if i != j and areEqual(seq1, j, seq2, i):
                    transpositions.append((token1, seq1[j]))
                matching_tokens.append(token1)
                
    jaro_m = len(matching_tokens)
    jaro_t = floor(len(transpositions)/2)
    
    jaro_dist = (jaro_m/size1 + jaro_m/size2 + (jaro_m-jaro_t)/jaro_m)/3
    
    jaro_p = coef
    jaro_l = prefix_len
    jaro_winkler_dist = jaro_dist + (jaro_l*jaro_p*(1-jaro_dist))
    
    return jaro_winkler_dist
    
###############################################################################
# COSINE SIMILARITY
###############################################################################
def cosine_similarity(seq1, seq2):
    """ 1 means that seq1 and seq2 are equal
    0 means that seq1 and seq2 are completely different
    """
    features = {token for token in seq1+seq2}
    
    vector_seq1 = np.zeros(len(features))
    vector_seq2 = np.zeros(len(features))
    for i, feature in enumerate(features):
            vector_seq1[i] = seq1.count(feature)
            vector_seq2[i] = seq2.count(feature)
    
    cos_sim = 1 - cosine(vector_seq1, vector_seq2)
    return cos_sim

###############################################################################
# HAMMING DISTANCE
###############################################################################
def hamming_distance(seq1, seq2):
    """ 0 means that seq1 and seq2 are equal
    seq1 and seq2 must be of equal lengths
    
    NB: Well suited for small sequences
    """
    assert len(seq1) == len(seq2)
    distance = 0
    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            distance += 1
    return distance

###############################################################################
# LEVENSHTEIN DISTANCE
###############################################################################
def levenshtein_similarity(seq1, seq2):
    """ 1 means that seq1 and seq2 are equal
    0 means that seq1 and seq2 are completely different
                              LD(term1,term2)
    sim(term1,term2) = 1 - ----------------------
                            max(|term1|,|term2|)
    """
    return 1 - (levenshtein_distance(seq1, seq2) / max(len(seq1), len(seq2)))

def levenshtein_distance(seq1, seq2):
    """ 0 means that seq1 and seq2 are equal
    
    NB: Well suited for small sequences
    """
    size1 = len(seq1) + 1
    size2 = len(seq2) + 1
    
    dist_mat = np.zeros((size1, size2))
    for i in range(size1):
        dist_mat[i, 0] = i
    for j in range(size2):
        dist_mat[0, j] = j
    
    for i in range(1, size1):
        for j in range(1, size2):
            cost = 0
            if seq1[i-1] != seq2[j-1]:
                cost = 1
            dist_mat[i][j] = min(dist_mat[i-1][j] + 1,      # Deletion
                                 dist_mat[i][j-1] + 1,      # Insertion
                                 dist_mat[i-1][j-1] + cost) # Substitution
    
    return dist_mat[size1-1][size2-1]

###############################################################################
# MINKOWSKI DISTANCE
###############################################################################
def minkowski_distance(seq1, seq2, p):
    """ 0 means that seq1 and seq2 are equal
    1 means that seq1 and seq2 are completely different
    """
    boi = list(set(seq1).union(set(seq2)))  # Bag of items
    
    fdist1 = FreqDist(seq1)
    fdist2 = FreqDist(seq2)
    
    inst1 = np.array([fdist1[item] for item in boi])
    inst2 = np.array([fdist2[item] for item in boi])
    
    distance = 0
    for i, freq in enumerate(inst1):
        distance += abs(inst1[i] - inst2[i]) ** p
    
    distance = distance ** (1/p)
    return distance

###############################################################################
# MANHATTAN DISTANCE
###############################################################################
def manhattan_distance(seq1, seq2):
    """ 0 means that seq1 and seq2 are equal
    1 means that seq1 and seq2 are completely different
    """
    return minkowski_distance(seq1, seq2, 1)

###############################################################################
# EUCLIDEAN DISTANCE
###############################################################################
def euclidean_distance(seq1, seq2):
    """ 0 means that seq1 and seq2 are equal
    1 means that seq1 and seq2 are completely different
    """
    return minkowski_distance(seq1, seq2, 2)