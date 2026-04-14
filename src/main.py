"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song


- recommend_songs
"""

import os
import sys

# Ensure the src/ directory is on the path so `recommender` is importable
# regardless of which directory the script is launched from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from recommender import load_songs, recommend_songs

# Resolve data path relative to this file so it works from any working directory
_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


_DIVIDER = "-" * 48
_MAX_SCORE = 6.0


def print_recommendation(rank: int, song: dict, score: float, explanation: str) -> None:
    """Render a single recommendation as a formatted card."""
    reasons = [r.strip() for r in explanation.split(" | ")]

    print(_DIVIDER)
    print(f"  #{rank:<3} {song['title']}")
    print(f"       {song.get('artist', 'Unknown Artist')}")
    print(f"       Score: {score:.2f} / {_MAX_SCORE:.1f}")
    print("       Why you'd like it:")
    for reason in reasons:
        print(f"         * {reason}")


def main() -> None:
    songs = load_songs(_DATA_PATH)
    print(f"Loaded {len(songs)} songs.")

    # --- User preference profiles ---

    # Profile 1: High-Energy Pop
    # Targets upbeat, danceable pop songs with high energy and positivity.
    high_energy_pop = {
        "name": "High-Energy Pop",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "likes_acoustic": False,
        "valence": 0.85,
    }

    # Profile 2: Chill Lofi
    # Targets relaxed, acoustic-leaning lofi tracks for low-key listening.
    chill_lofi = {
        "name": "Chill Lofi",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
        "valence": 0.60,
    }

    # Profile 3: Deep Intense Rock
    # Targets heavy, high-tempo rock songs with low acousticness.
    deep_intense_rock = {
        "name": "Deep Intense Rock",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "likes_acoustic": False,
        "valence": 0.40,
    }

    # -------------------------------------------------------
    # ADVERSARIAL / EDGE-CASE PROFILES
    # Each one is designed to expose a specific weakness in
    # the scoring logic.
    # -------------------------------------------------------

    # Adversarial 1: Nonexistent Mood
    # "sad" does not appear in songs.csv — mood points are silently 0
    # for every song. The algorithm will never mention the mismatch.
    # Expected flaw: recommends high-energy songs (energy proximity win)
    # even though the user explicitly wants a "sad" mood.
    sad_headbanger = {
        "name": "ADVERSARIAL — Nonexistent Mood",
        "genre": "rock",
        "mood": "sad",          # No song has mood="sad"
        "energy": 0.90,
        "likes_acoustic": False,
        "valence": 0.15,
    }

    # Adversarial 2: Out-of-Range Energy
    # energy=1.5 is above the valid [0.0, 1.0] scale.
    # Formula: 1.5 * (1 - |1.5 - song_energy|)
    # For a low-energy song (e.g. energy=0.28):
    #   1.5 * (1 - 1.22) = 1.5 * -0.22 = -0.33  ← NEGATIVE contribution
    # The formula was designed to only reward; out-of-range input
    # accidentally penalizes songs instead of ignoring them.
    out_of_range_energy = {
        "name": "ADVERSARIAL — Out-of-Range Energy",
        "genre": "pop",
        "mood": "happy",
        "energy": 1.5,          # Above max; will produce negative energy pts
        "likes_acoustic": False,
        "valence": 1.2,         # Also out of range
    }

    # Adversarial 3: Case-Sensitivity Trap
    # genre="Pop" and mood="Happy" use capital letters.
    # score_song() does an exact string comparison; songs.csv stores
    # everything lowercase, so both fields score 0 for every song.
    # The system silently falls back to energy/acousticness/valence.
    case_mismatch = {
        "name": "ADVERSARIAL — Case Mismatch",
        "genre": "Pop",         # CSV has "pop" — will never match
        "mood": "Happy",        # CSV has "happy" — will never match
        "energy": 0.85,
        "likes_acoustic": False,
        "valence": 0.80,
    }

    # Adversarial 4: Conflicting Energy + Acoustic Preference
    # energy=0.92 (very high) + likes_acoustic=True creates a contradiction:
    # high-energy songs (rock/metal/electronic ~0.91-0.94) have very low
    # acousticness (~0.08-0.15), so the two signals pull in opposite directions.
    # Watch which signal wins and whether the explanation makes it obvious.
    acoustic_headbanger = {
        "name": "ADVERSARIAL — Acoustic + High Energy Conflict",
        "genre": "folk",
        "mood": "introspective",
        "energy": 0.92,         # Extreme high energy...
        "likes_acoustic": True, # ...but also wants acoustic
        "valence": 0.65,
    }

    # Adversarial 5: Conflicting Mood + Valence
    # mood="happy" steers toward cheerful songs (Sunrise City valence=0.84),
    # but valence=0.05 (near zero) pulls toward very dark/negative songs.
    # The algorithm will pick the mood-matching song and give it almost 0
    # valence points — or pick a dark song with no mood match.
    # Either way the profile's intent is internally contradictory and the
    # explanation won't flag the inconsistency.
    happy_but_sad = {
        "name": "ADVERSARIAL — Happy Mood, Sad Valence",
        "genre": "pop",
        "mood": "happy",        # Mood says cheerful...
        "energy": 0.80,
        "likes_acoustic": False,
        "valence": 0.05,        # ...but valence says extremely dark/negative
    }

    # Adversarial 6: Genre Not in Catalog
    # "k-pop" does not exist in songs.csv. Every song scores 0 for genre
    # (the biggest single weight: 2.0 pts). The algorithm confidently
    # returns a ranked list with no warning that the desired genre is absent.
    genre_not_found = {
        "name": "ADVERSARIAL — Genre Not in Catalog",
        "genre": "k-pop",       # Not in songs.csv
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
        "valence": 0.80,
    }

    profiles = [
        high_energy_pop,
        chill_lofi,
        deep_intense_rock,
        sad_headbanger,
        out_of_range_energy,
        case_mismatch,
        acoustic_headbanger,
        happy_but_sad,
        genre_not_found,
    ]

    for user_prefs in profiles:
        print(f"\n{'=' * 48}")
        print(f"  Profile: {user_prefs['name']}")
        print(f"  genre={user_prefs['genre']}  mood={user_prefs['mood']}  "
              f"energy={user_prefs['energy']}  "
              f"likes_acoustic={user_prefs['likes_acoustic']}  "
              f"valence={user_prefs['valence']}")
        print(f"\n  Top 5 Recommendations")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        for rank, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            print_recommendation(rank, song, score, explanation)

        print(_DIVIDER)


if __name__ == "__main__":
    main()
