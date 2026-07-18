"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 48
    print("\n" + "─" * width)
    print(f"  Top {len(recommendations)} Recommendations")
    print("─" * width)

    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        title  = song.get('title',  'Unknown')
        artist = song.get('artist', 'Unknown')
        print(f"\n  {i}. {title} — {artist}")
        print(f"     Score  : {score:.2f} / 4.0")
        print(f"     Why    : {' | '.join(reasons)}")

    print("\n" + "─" * width + "\n")


if __name__ == "__main__":
    main()
