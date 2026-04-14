"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop {len(recommendations)} recommendations for: genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print("=" * 55)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} - {song['artist']}")
        print(f"    Score : {score:.1f} / 100")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"    Why   : {explanation}")


if __name__ == "__main__":
    main()
