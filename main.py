from src.load_data import load_user_artists, load_artists
from src.identity import build_identity_vector, get_user_profile
from src.recommender import build_user_matrix, recommend_artists
from src.attack import inject_playcount
from src.metrics import identity_drift, recommendation_overlap

# Load data
ua = load_user_artists("data/hetrec2011/user_artists.dat")
artists = load_artists("data/hetrec2011/artists.dat")

users = ua["user_id"].unique()
artist_ids = ua["artist_id"].unique()

# Pick a victim user
victim = users[0]

# Baseline identity
id_before = build_identity_vector(ua, victim, artist_ids)

matrix, user_index, artist_index = build_user_matrix(ua, users, artist_ids)
rec_before = recommend_artists(victim, matrix, user_index, artist_index)

# Attack
target_artist = artist_ids[-1]  # Not listened to often
ua_attacked = inject_relative_playcount(ua, victim, target_artist, injection_count=20)

# After attack
id_after = build_identity_vector(ua_attacked, victim, artist_ids)
matrix_attacked, _, _ = build_user_matrix(ua_attacked, users, artist_ids)
rec_after = recommend_artists(victim, matrix_attacked, user_index, artist_index)

print("Identity drift:", identity_drift(id_before, id_after))
print("Recommendation overlap:", recommendation_overlap(rec_before, rec_after))
