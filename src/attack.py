def inject_relative_playcount(user_id, artist_id, fraction=0.2):
    global user_artists

    user_total = user_artists[
        user_artists["user_id"] == user_id
    ]["playcount"].sum()

    injection = int(user_total * fraction)

    mask = (
        (user_artists["user_id"] == user_id) &
        (user_artists["artist_id"] == artist_id)
    )

    if mask.any():
        user_artists.loc[mask, "playcount"] += injection
    else:
        user_artists = pd.concat(
            [user_artists, pd.DataFrame([{
                "user_id": user_id,
                "artist_id": artist_id,
                "playcount": injection
            }])],
            ignore_index=True
        )

    return injection
def find_boundary_artists(user_id, top_n=5):
    u_idx = user_index[user_id]
    sims = cosine_similarity([user_matrix[u_idx]], user_matrix)[0]

    # Top similar users (excluding self)
    similar_users = sims.argsort()[-20:-1]

    candidate_scores = {}

    for su in similar_users:
        listened = user_matrix[su]
        for ai, val in enumerate(listened):
            if val > 0 and user_matrix[u_idx][ai] == 0:
                candidate_scores[ai] = candidate_scores.get(ai, 0) + val

    top_candidates = sorted(
        candidate_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return [all_artist_ids[i] for i, _ in top_candidates]
def boundary_injection_attack(user_id, injection_per_artist=50):
    candidates = find_boundary_artists(user_id)

    for artist_id in candidates:
        inject_playcount(user_id, artist_id, injection_per_artist)

    return candidates
