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

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print(f"\nProfile -> genre={user_prefs['genre']}  "
          f"mood={user_prefs['mood']}  energy={user_prefs['energy']}")
    print(f"\nTop 5 Recommendations")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print_recommendation(rank, song, score, explanation)

    print(_DIVIDER)


if __name__ == "__main__":
    main()
