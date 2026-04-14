from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the song catalog for later scoring."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by how well they match the user's profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language string describing why this song suits the user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    # Columns that must be floats so math operations work correctly
    float_fields = {
        "energy", "tempo_bpm", "valence", "danceability",
        "acousticness", "instrumentalness", "speechiness",
        "liveness", "loudness",
    }
    # Columns that must be integers
    int_fields = {"id", "popularity"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in float_fields:
                if row.get(field) is not None:
                    row[field] = float(row[field])
            for field in int_fields:
                if row.get(field) is not None:
                    row[field] = int(row[field])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against a user preference dictionary.

    Algorithm Recipe (max 6.0 points total):
      +2.0  genre match          (exact)
      +1.0  mood match           (exact)
      +1.5  energy proximity     (1.5 × (1 - |target - song|))
      +1.0  acousticness         (direction: high if likes_acoustic, low if not)
      +0.5  valence proximity    (0.5 × (1 - |target - song|))

    Returns (score, explanation) so the caller knows why a song ranked where it did.
    """
    score = 0.0
    reasons = []

    # Rule 1 — Genre match: +2.0 points
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match ({song['genre']})")

    # Rule 2 — Mood match: +1.0 point
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match ({song['mood']})")

    # Rule 3 — Energy proximity: up to 1.5 points
    # Rewards closeness to the user's target, not high or low energy in isolation
    target_energy = user_prefs.get("energy", 0.5)
    energy_pts = 1.5 * (1 - abs(target_energy - song["energy"]))
    score += energy_pts
    reasons.append(f"energy {song['energy']} (target {target_energy}, +{energy_pts:.2f}pts)")

    # Rule 4 — Acousticness direction: up to 1.0 point
    # likes_acoustic=True  → high acousticness is rewarded
    # likes_acoustic=False → low acousticness is rewarded
    if user_prefs.get("likes_acoustic", False):
        acou_pts = 1.0 * song["acousticness"]
        reasons.append(f"acoustic-friendly ({song['acousticness']:.2f})")
    else:
        acou_pts = 1.0 * (1 - song["acousticness"])
        reasons.append(f"electronic-friendly ({1 - song['acousticness']:.2f})")
    score += acou_pts

    # Rule 5 — Valence proximity: up to 0.5 points (tiebreaker)
    target_valence = user_prefs.get("valence", 0.5)
    valence_pts = 0.5 * (1 - abs(target_valence - song["valence"]))
    score += valence_pts

    explanation = " | ".join(reasons)
    return round(score, 4), explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts by score descending, and returns the top k.
    Required by src/main.py — return format: (song_dict, score, explanation)

    sorted() is used instead of .sort() because:
      - sorted() returns a new list without mutating the original catalog
      - it can be chained directly with [:k], keeping the logic in one expression
      - .sort() modifies in-place and returns None, which would require two steps
    """
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
