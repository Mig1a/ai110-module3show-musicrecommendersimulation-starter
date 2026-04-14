# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version implements a **weighted proximity recommender** called *VibeFinder 1.0*. It represents each song as a set of five features — genre, mood, energy, valence, and acousticness — and scores every song against a user's taste profile using a weighted sum. Categorical features (genre, mood) contribute via exact match (1.0 or 0.0), while numerical features (energy, valence, acousticness) are scored by proximity: the closer a song's value is to the user's target, the higher it scores. Feature weights are 30% genre, 25% mood, 25% energy, 10% valence, and 10% acousticness, reflecting the intuition that genre and mood are near-hard constraints while numerical similarity acts as a tiebreaker. All songs in the 10-song catalog are scored independently, then sorted by descending score, and the top k results are returned with a plain-language explanation of why each song ranked where it did.

---

## How The System Works

VibeFinder 1.0 is a content-based recommender — it matches users to songs purely by comparing feature values, with no knowledge of what other users have listened to.

**What each `Song` stores:**
- `genre` — the musical category (pop, lofi, rock, ambient, jazz, synthwave, indie pop, and more)
- `mood` — the emotional context (happy, chill, intense, relaxed, focused, moody, and more)
- `energy` — a 0–1 float measuring how energetic or calm the track feels
- `valence` — a 0–1 float measuring emotional positivity (high = upbeat, low = darker)
- `acousticness` — a 0–1 float measuring how organic vs. electronic the production sounds

**What the `UserProfile` stores:**
- `favorite_genre` — the genre the user prefers
- `favorite_mood` — the mood they are looking for right now
- `target_energy` — a 0–1 float for how energetic they want the music
- `target_valence` — a 0–1 float for the emotional tone they want
- `likes_acoustic` — a boolean for whether they prefer organic or electronic sound

---

### Algorithm Recipe

Every song in the catalog is run through the same five rules. Points are added up to produce a final score out of **6.0**.

**Rule 1 — Genre Match: +2.0 points**
```
genre_points = 2.0 if song.genre == user.favorite_genre else 0.0
```
Highest single bonus. Genre is the listener's identity — a metal fan and a jazz fan share almost no overlap. No partial credit.

**Rule 2 — Mood Match: +1.0 point**
```
mood_points = 1.0 if song.mood == user.favorite_mood else 0.0
```
Half the value of genre. Mood is context-driven and changes session to session, but still shapes the vibe meaningfully.

**Rule 3 — Energy Proximity: 0.0 to +1.5 points**
```
energy_points = 1.5 × (1 - |user.target_energy - song.energy|)
```
Proximity scoring — does not reward high or low energy, only closeness to the user's target. Energy earns the highest numerical weight because it has the widest spread (0.28–0.94) across the catalog.

**Rule 4 — Acousticness Direction: 0.0 to +1.0 point**
```
if user.likes_acoustic:
    acousticness_points = 1.0 × song.acousticness
else:
    acousticness_points = 1.0 × (1 - song.acousticness)
```
Direction-based scoring — both extremes are valid, just for different users. An electronic fan is rewarded the same way an acoustic fan is, just in the opposite direction.

**Rule 5 — Valence Proximity: 0.0 to +0.5 points**
```
valence_points = 0.5 × (1 - |user.target_valence - song.valence|)
```
Tiebreaker only. Valence has a narrower spread in the catalog so it contributes less discrimination. Capped at 0.5 so it never overrides a genre or mood signal.

**Final score:**
```
score = genre_points + mood_points + energy_points + acousticness_points + valence_points
```

| Feature | Max Points | Share of Total |
|---|---|---|
| Genre | 2.0 | 33% |
| Energy | 1.5 | 25% |
| Mood | 1.0 | 17% |
| Acousticness | 1.0 | 17% |
| Valence | 0.5 | 8% |
| **Total** | **6.0** | **100%** |

**How songs are ranked and returned:**

Every song is scored independently, sorted by score from highest to lowest, and the top k results are returned with a plain-language explanation of which features drove the score.

---

### Potential Biases

- **Genre over-dominance.** At 33% of the total score, a genre match adds 2.0 points before any other rule runs. A song that perfectly matches the user's energy, mood, and acousticness but is in a different genre will be buried under any genre match — even a weak one. This means the system can miss great songs that are adjacent to the user's preferred genre (e.g., ambient surfaced to a lofi listener).

- **Exact-match blindness.** Both genre and mood award 1.0 or 0.0 with no partial credit. "Focused" and "chill" are close moods, but the system treats them as completely different. The same applies to genre neighbors like jazz and lofi. This creates hard invisible walls in the catalog.

- **Catalog size amplifies both problems.** With only 18 songs, some genres and moods appear just once. A user whose favorite genre is "classical" will only ever get one genre-match bonus in the entire catalog, pushing every recommendation toward numerical similarity rather than identity — which is the opposite problem from genre over-dominance.

- **No listening history.** The system knows nothing about what the user has already heard. It can recommend the same song twice across sessions and has no way to introduce variety over time.

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

## Sample Output

The following is the actual terminal output for the starter profile
(`genre=pop`, `mood=happy`, `energy=0.8`):

![Terminal screenshot showing top 5 recommendations](<terminal _SS.png>)

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


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

