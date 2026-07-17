import csv
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
    favorite_genre: str = "lofi"
    favorite_mood: str = "chill"
    target_energy: float = 0.35
    likes_acoustic: bool = True

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    # Scores one song for one user: adds points for genre match, mood match, and how close the energy is
    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += GENRE_MATCH_POINTS
            reasons.append(f"genre match (+{GENRE_MATCH_POINTS:.1f})")

        if song.mood == user.favorite_mood:
            score += MOOD_MATCH_POINTS
            reasons.append(f"mood match (+{MOOD_MATCH_POINTS:.1f})")

        energy_distance = abs(song.energy - user.target_energy)
        energy_points = ENERGY_MATCH_POINTS * (1 - energy_distance)
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

        return score, reasons

    # Scores every song, sorts best-to-worst, and returns the top k songs
    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    # Builds a plain-English reason for why one song was recommended to one user
    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score(user, song)
        return ", ".join(reasons)

NUMERIC_SONG_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

# Reads the songs CSV file and turns each row into a dictionary with the right types (numbers, not text)
def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row["id"] = int(row["id"])
            for field in NUMERIC_SONG_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs

GENRE_MATCH_POINTS = 2.0
MOOD_MATCH_POINTS = 1.0
ENERGY_MATCH_POINTS = 1.0

# Scores one song dict for one user dict: same genre/mood/energy rule as Recommender._score, but on dicts
def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += GENRE_MATCH_POINTS
        reasons.append(f"genre match (+{GENRE_MATCH_POINTS:.1f})")

    if song["mood"] == user_prefs["mood"]:
        score += MOOD_MATCH_POINTS
        reasons.append(f"mood match (+{MOOD_MATCH_POINTS:.1f})")

    energy_distance = abs(song["energy"] - user_prefs["energy"])
    energy_points = ENERGY_MATCH_POINTS * (1 - energy_distance)
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    return score, reasons

# Scores every song, sorts best-to-worst, and returns the top k as (song, score, explanation) tuples
def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
