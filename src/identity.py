import numpy as np
import pandas as pd

def get_user_profile(user_artists, user_id, artists_df, top_k=10):
    user_data = user_artists[user_artists["user_id"] == user_id]
    user_data = user_data.merge(artists_df, on="artist_id")

    user_data = user_data.sort_values("playcount", ascending=False)
    return user_data[["artist_id", "name", "playcount"]].head(top_k)

def build_identity_vector(user_artists, user_id, all_artist_ids):
    user_data = user_artists[user_artists["user_id"] == user_id]

    vector = np.zeros(len(all_artist_ids))
    artist_index = {a: i for i, a in enumerate(all_artist_ids)}

    total = user_data["playcount"].sum()

    for _, row in user_data.iterrows():
        idx = artist_index[row["artist_id"]]
        vector[idx] = row["playcount"] / total

    return vector
