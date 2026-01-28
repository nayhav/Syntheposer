import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def build_user_matrix(user_artists, all_users, all_artists):
    matrix = np.zeros((len(all_users), len(all_artists)))

    user_index = {u: i for i, u in enumerate(all_users)}
    artist_index = {a: i for i, a in enumerate(all_artists)}

    for _, row in user_artists.iterrows():
        ui = user_index[row["user_id"]]
        ai = artist_index[row["artist_id"]]
        matrix[ui, ai] = row["playcount"]

    matrix = matrix / (matrix.sum(axis=1, keepdims=True) + 1e-8)
    return matrix, user_index, artist_index


def recommend_artists(user_id, matrix, user_index, artist_index, top_k=10):
    u_idx = user_index[user_id]
    sims = cosine_similarity([matrix[u_idx]], matrix)[0]

    scores = sims @ matrix
    scores[u_idx] = 0  # don't recommend self

    top_indices = scores.argsort()[-top_k:][::-1]
    inv_artist_index = {i: a for a, i in artist_index.items()}

    return [inv_artist_index[i] for i in top_indices]
