import pandas as pd

def load_user_artists(path):
    return pd.read_csv(
        path,
        sep="\t",
        names=["user_id", "artist_id", "playcount"],
        header=0
    )

def load_artists(path):
    return pd.read_csv(
        path,
        sep="\t",
        names=["artist_id", "name", "url", "picture_url"],
        header=0
    )

def load_tags(path):
    return pd.read_csv(
        path,
        sep="\t",
        names=["tag_id", "tag"],
        header=0
    )
