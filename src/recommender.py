from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """Represents a song with audio attributes."""
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
    """Represents a user's music taste preferences."""
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
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Generate recommended songs for a user."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load and parse songs from a CSV file."""
    import csv

    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song based on user preferences."""
    score = 0.0
    reasons = []

    # Genre exact match: +30 pts
    if song["genre"] == user_prefs.get("genre", ""):
        score += 30
        reasons.append("genre match (+30)")

    # Mood exact match: +40 pts
    mood_match = song["mood"] == user_prefs.get("mood", "")
    if mood_match:
        score += 40
        reasons.append("mood match (+40)")

    # Energy proximity: 0–20 pts
    energy_pts = (1 - abs(user_prefs.get("energy", 0.5) - song["energy"])) * 20
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.1f})")

    # Attribute bonuses: up to +10 pts (only stack when mood already matches)
    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.7:
        score += 5
        reasons.append("acoustic match (+5)")

    if mood_match and song["valence"] > 0.7:
        score += 3
        reasons.append("high valence bonus (+3)")

    if mood_match and song["danceability"] > 0.7:
        score += 2
        reasons.append("high danceability bonus (+2)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank and return top k recommended songs."""
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    return ranked[:k]
