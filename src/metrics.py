import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def identity_drift(vec_before, vec_after):
    return 1 - cosine_similarity([vec_before], [vec_after])[0][0]


def recommendation_overlap(rec_before, rec_after):
    return len(set(rec_before).intersection(set(rec_after)))
