import csv
import math
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
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(filepath: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    float_fields = {'energy', 'tempo_bpm', 'valence', 'danceability', 'acousticness'}
    int_fields = {'id'}
    songs = []
    with open(filepath, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            song = {}
            for key, value in row.items():
                if key in float_fields:
                    try:
                        song[key] = float(value)
                    except (ValueError, TypeError):
                        song[key] = 0.0
                elif key in int_fields:
                    try:
                        song[key] = int(value)
                    except (ValueError, TypeError):
                        song[key] = 0
                else:
                    song[key] = value
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if song.get('genre', '').lower() == user_prefs.get('genre', '').lower():
        score += 1.0
        reasons.append('Genre match (+1.0)')

    if song.get('mood', '').lower() == user_prefs.get('mood', '').lower():
        score += 1.0
        reasons.append('Mood match (+1.0)')

    song_energy = song.get('energy', 0.0)
    target_energy = user_prefs.get('energy', 0.0)
    energy_points = 2.0 * math.exp(-((song_energy - target_energy) ** 2) / (2 * 0.15 ** 2))
    score += energy_points
    reasons.append(f'Energy match (+{energy_points:.2f})')

    return (round(score, 4), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
