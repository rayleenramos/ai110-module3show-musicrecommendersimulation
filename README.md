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

Real-world recommenders (like Spotify or Netflix) work by turning both the items and the user into data, then measuring how well they match. They generally use two big strategies: content-based filtering, which compares an item's attributes (genre, mood, tempo, etc.) directly against a user's stated or inferred preferences, and collaborative filtering, which looks at patterns across many users to guess "people similar to you also liked this." Real systems usually blend both, plus signals like recency, popularity, and past engagement (skips, replays, likes) to keep refining the match over time.

My version is a simplified, content-based recommender. It does not learn from other users or from listening history, it only compares each song's attributes against one user's stated taste profile. I'm prioritizing three features that matter most for "does this song fit what the user is looking for right now": **genre**, **mood**, and **energy**. Each song gets a score built from how well it matches on these three dimensions, and the highest-scoring songs are ranked and returned as recommendations.

- **`Song`** features used: `genre`, `mood`, `energy` 
- **`UserProfile`** features used: `favorite_genre`, `favorite_mood`, `target_energy`
- The `Recommender` scores each song by combining a genre match, a mood match, and a distance-based energy score (closer to `target_energy` = higher score), then ranks songs by total score and returns the top `k`.

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

Output from running `python -m src.main`, which loops through three distinct example profiles defined in `USER_PROFILES`:

### High-Energy Pop (`genre=pop, mood=happy, energy=0.8`)

```
Top recommendations:

Sunrise City - Score: 3.98
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

Gym Hero - Score: 2.87
Because: genre match (+2.0), energy similarity (+0.87)

Rooftop Lights - Score: 1.96
Because: mood match (+1.0), energy similarity (+0.96)

Concrete Kingdom - Score: 1.00
Because: energy similarity (+1.00)

Night Drive Loop - Score: 0.95
Because: energy similarity (+0.95)
```

### Chill Lofi (`genre=lofi, mood=chill, energy=0.35`)

```
Top recommendations:

Library Rain - Score: 4.00
Because: genre match (+2.0), mood match (+1.0), energy similarity (+1.00)

Midnight Coding - Score: 3.93
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.93)

Focus Flow - Score: 2.95
Because: genre match (+2.0), energy similarity (+0.95)

Spacewalk Thoughts - Score: 1.93
Because: mood match (+1.0), energy similarity (+0.93)

Coffee Shop Stories - Score: 0.98
Because: energy similarity (+0.98)
```

### Deep Intense Rock (`genre=rock, mood=intense, energy=0.9`)

```
Top recommendations:

Storm Runner - Score: 3.99
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.99)

Gym Hero - Score: 1.97
Because: mood match (+1.0), energy similarity (+0.97)

Neon Pulse Rave - Score: 0.98
Because: energy similarity (+0.98)

Iron Cathedral - Score: 0.93
Because: energy similarity (+0.93)

Sunrise City - Score: 0.92
Because: energy similarity (+0.92)
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



