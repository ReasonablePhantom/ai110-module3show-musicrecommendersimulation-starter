# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### Song Features

Each song in the catalog stores five attributes:

| Feature | Type | Description |
|---|---|---|
| `genre` | string | Musical category (Rock, Jazz, Ambient, etc.) |
| `mood` | string | Emotional label (melancholic, euphoric, aggressive, etc.) |
| `energy` | float 0.0–1.0 | Intensity — 0.0 is completely calm, 1.0 is maximum intensity |
| `tempo_bpm` | int | Beats per minute |
| `valence` | float 0.0–1.0 | Emotional positivity — 0.0 is dark/sad, 1.0 is bright/happy |

---

### User Taste Profile

The user profile stores preferences as a dictionary:

```python
{
    'favorite_genre':   'Rock',    # string — preferred genre
    'favorite_mood':    'Intense', # string — preferred mood label
    'target_energy':    0.85,      # float  — ideal energy level
    'target_valence':   0.20,      # float  — ideal emotional tone
    'target_tempo_bpm': 160        # int    — ideal tempo
}
```

---

### Scoring Rule (one song at a time)

Every song receives a score out of a maximum of **4.0 points**:

| Component | Points | Rule |
|---|---|---|
| Genre match | +2.0 | Exact string match with `favorite_genre` |
| Mood match | +1.0 | Exact string match with `favorite_mood` |
| Energy proximity | 0.0–1.0 | Gaussian decay formula (see below) |

**Energy proximity formula:**

```
energy_score = exp( -(song.energy - target_energy)² / 0.045 )
```

This uses a Gaussian bell curve with σ = 0.15. A song whose energy exactly matches the target scores 1.0. A song 0.30 units away scores ~0.135. A song 0.50 units away scores near 0.

---

### Data Flow

```
Input: User Taste Profile
        │
        ▼
Load Song Catalog (N songs)
        │
        ▼
For each song:
  ├── genre_score  = 2.0 if genre matches, else 0.0
  ├── mood_score   = 1.0 if mood matches,  else 0.0
  └── energy_score = exp(-(energy − target)² / 0.045)
        │
        ▼
total_score = genre_score + mood_score + energy_score
        │
        ▼
Sort all songs by total_score (highest first)
        │
        ▼
Output: Top K songs as the recommendation list
```

---

### Potential Biases

> **Genre over-prioritization:** The genre match bonus (+2.0) is twice the maximum energy score (+1.0). This means a mediocre genre match always outranks a perfect cross-genre match. For example, a Jazz track with energy=0.85 (perfect energy alignment) scores only 1.0, while a Rock track with energy=0.20 (poor energy alignment) scores 2.135 — and still wins. This system might over-prioritize genre matching, potentially ignoring high-energy songs from other genres that perfectly match the user's mood and energy preferences.

> **Mood label rigidity:** Mood is matched as an exact string. "Intense" and "aggressive" might feel identical to a listener but score 0 for each other. Encoding mood as a continuous valence score would be more robust.

> **Cold-start gap:** New songs or users with no preference history cannot be scored meaningfully — the profile must be pre-populated.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



