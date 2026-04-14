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

![Screenshot 2026-04-14 153707](<Screenshot 2026-04-14 153707.png>)

![Screenshot 2026-04-14 153735](<Screenshot 2026-04-14 153735.png>)

![Screenshot 2026-04-14 153750](<Screenshot 2026-04-14 153750.png>)

![Screenshot 2026-04-14 153804](<Screenshot 2026-04-14 153804.png>)

![Screenshot 2026-04-14 153819](<Screenshot 2026-04-14 153819.png>)

![Screenshot 2026-04-14 153836](<Screenshot 2026-04-14 153836.png>)

![Screenshot 2026-04-14 153851](<Screenshot 2026-04-14 153851.png>)

![Screenshot 2026-04-14 153909](<Screenshot 2026-04-14 153909.png>)

![Screenshot 2026-04-14 153935](<Screenshot 2026-04-14 153935.png>)

---

## Experiments You Tried

---

### Experiment 1 — Genre Weight: 2.0 → 0.5

**Change:** Reduced the genre match bonus from `+2.0` to `+0.5`. The new maximum score drops from 6.0 to 4.5 points.

**What happened:**

| Profile | Baseline Top 5 | Exp 1 Top 5 | Key Shift |
|---|---|---|---|
| High-Energy Pop | Sunrise City, **Gym Hero**, Rooftop Lights, Electric Surge, Storm Runner | Sunrise City, **Rooftop Lights**, Gym Hero, Electric Surge, Storm Runner | Rooftop Lights (indie pop/happy) jumps to #2, pushing Gym Hero (pop/intense) to #3 |
| Chill Lofi | Library Rain, Midnight Coding, Focus Flow, **Spacewalk Thoughts**, Coffee Shop | Library Rain, Midnight Coding, **Spacewalk Thoughts**, Focus Flow, Coffee Shop | Spacewalk Thoughts (ambient/chill) rises from #4 to #3, leapfrogging Focus Flow |
| Deep Intense Rock | Storm Runner, Gym Hero, Metallic Fury, Electric Surge, Bass Rebellion | Storm Runner, Gym Hero, Metallic Fury, Electric Surge, Bass Rebellion | No change — energy + mood proximity already separated these songs |

**Interpretation:**

When genre weight drops to 0.5, mood matching and numerical proximity become the dominant signal. For **High-Energy Pop**, Rooftop Lights (indie pop, mood=happy) now outranks Gym Hero (pop, mood=intense) because a mood match (+1.0) is worth double the reduced genre bonus (+0.5). For **Chill Lofi**, Spacewalk Thoughts (ambient, mood=chill) benefits from the same shift — it was being suppressed by Focus Flow's lofi genre match, but now the chill mood match levels the playing field. For **Deep Intense Rock**, the rankings stay the same because Storm Runner earns both the genre and mood match anyway, and the remaining songs are separated by energy proximity regardless of the genre weight.

**Conclusion:** At 2.0, genre acts like a hard filter — a wrong-genre song almost never beats a same-genre song. At 0.5, cross-genre songs with strong mood or energy matches can break through. This is more surprising and arguably more useful when the catalog is small.

---

### Experiment 2 — Added Tempo Proximity Rule

**Change:** Added a new scoring rule based on `tempo_bpm` from the CSV (previously loaded but ignored). Rule: `tempo_pts = 0.5 * max(0, 1 - |target_tempo - song_tempo| / 100)`. New maximum score is 6.5 points. Each profile was given a realistic `target_tempo`.

| Profile | Target Tempo | Rationale |
|---|---|---|
| High-Energy Pop | 128 BPM | Standard danceable pop tempo |
| Chill Lofi | 75 BPM | Slow, relaxed lofi tempo |
| Deep Intense Rock | 150 BPM | Fast, driving rock/metal tempo |

**What happened:**

| Profile | Baseline Top 5 | Exp 2 Top 5 | Key Shift |
|---|---|---|---|
| High-Energy Pop | ... #5 **Storm Runner** (152 BPM) | ... #5 **Bass Rebellion** (115 BPM) | Storm Runner's tempo (152) is 24 BPM off target 128; Bass Rebellion (115) is only 13 BPM off, pushing it up |
| Chill Lofi | Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts, Coffee Shop | Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts, Coffee Shop | No ranking change — the lofi/chill songs that already dominated also happen to cluster around 72–80 BPM, perfectly close to target 75 |
| Deep Intense Rock | Storm Runner, Gym Hero, Metallic Fury, Electric Surge, Bass Rebellion | Storm Runner, Gym Hero, Metallic Fury, Electric Surge, Bass Rebellion | No ranking change — Storm Runner (152 BPM) is the closest song to the 150 BPM target, reinforcing its #1 position |

**Detailed score changes for High-Energy Pop:**

| Song | Baseline Score | Exp 2 Score | Tempo Contribution |
|---|---|---|---|
| Sunrise City | 5.70 | 6.14 | +0.45 (118 BPM, 10 off) |
| Gym Hero | 4.87 | 5.34 | +0.48 (132 BPM, 4 off) |
| Rooftop Lights | 3.42 | 3.90 | +0.48 (124 BPM, 4 off) |
| Electric Surge | 2.89 | 3.34 | +0.45 (138 BPM, 10 off) |
| Storm Runner | 2.70 | 2.94 | +0.24 (152 BPM, 24 off) |
| Bass Rebellion | — | 3.09 | +0.43 (115 BPM, 13 off) |

**Interpretation:**

Tempo reinforced existing preferences in two of three profiles — songs that were already winning also happened to have suitable tempos. The only visible disruption was at the bottom of the High-Energy Pop list, where Storm Runner (a 152 BPM rock track) was penalized and Bass Rebellion (115 BPM hip hop) replaced it at #5. This shows that tempo is most impactful as a tiebreaker at the margins rather than a rank-reversing force, unless the target tempo strongly separates songs that are otherwise equally matched.

**Conclusion:** Adding tempo improved score resolution (songs now spread from 2.94 to 6.14 instead of 2.70 to 5.70) without disrupting established rankings except at the edges. Tempo works best when the user's preferred genre has a distinctive BPM range (e.g., lofi at ~70–80 BPM vs. metal at 150+ BPM).

---

### Experiment 3 — System Behavior Across Different User Types

Nine profiles were tested: three realistic profiles and six adversarial profiles designed to expose weaknesses. Results from `python -m src.main` are summarized below.

#### Profile 1: High-Energy Pop (genre=pop, mood=happy, energy=0.90, likes_acoustic=False, valence=0.85)
**Top result:** Sunrise City — 5.70 / 6.0
**Behavior:** The system worked exactly as intended. Only two pop songs exist (Sunrise City and Gym Hero); both rose to #1 and #2. Sunrise City won because it also matched the happy mood (+1.0 extra over Gym Hero). Non-pop songs were all below 3.5 regardless of energy match.

#### Profile 2: Chill Lofi (genre=lofi, mood=chill, energy=0.35, likes_acoustic=True, valence=0.60)
**Top result:** Library Rain — 5.86 / 6.0
**Behavior:** Near-perfect result. Library Rain matched genre, mood, energy (exact 0.35), and acousticness (0.86) simultaneously. All three lofi songs occupied the top 3. The only non-lofi song to break into the top 5 was Spacewalk Thoughts (ambient/chill, #4) thanks to its chill mood match and very high acousticness (0.92).

#### Profile 3: Deep Intense Rock (genre=rock, mood=intense, energy=0.92, likes_acoustic=False, valence=0.40)
**Top result:** Storm Runner — 5.84 / 6.0
**Behavior:** Near-perfect result. Storm Runner is the only rock/intense song in the catalog and claimed an unbeatable lead. Gym Hero (pop/intense, #2 at 3.75) shows that mood match alone can elevate a song significantly even without genre alignment.

#### Adversarial 1: Nonexistent Mood (mood="sad")
**Top result:** Storm Runner — 4.72 / 6.0
**Behavior:** "Sad" does not appear in songs.csv, so zero mood points were awarded to any song. The system recommended high-energy rock tracks (Storm Runner, Metallic Fury, Gym Hero) based purely on genre and energy proximity — completely ignoring that the user's requested mood was never matched. No warning or fallback was triggered.

**Flaw exposed:** The system silently accepts an impossible mood constraint and never tells the user it found zero matches for it. A real system would surface a warning: "No songs found with mood 'sad'."

#### Adversarial 2: Out-of-Range Energy (energy=1.5, valence=1.2)
**Top result:** Sunrise City — 4.62 / 6.0 (down from 5.70 in baseline)
**Behavior:** Genre and mood matches still drove the top results, but all energy scores collapsed. The highest-energy song in the catalog (Metallic Fury at 0.94) was still 0.56 below the 1.5 target, yielding only 0.69 energy points instead of the usual ~1.47. Low-energy songs produced negative energy contributions (e.g., Spacewalk Thoughts at 0.28 scored `1.5 × (1 - 1.22) = -0.33`). The formula was designed for [0.0, 1.0] and silently misbehaves outside that range.

**Flaw exposed:** Out-of-range inputs are not clamped or rejected — they quietly degrade and invert the scoring for some songs.

#### Adversarial 3: Case Mismatch (genre="Pop", mood="Happy")
**Top result:** Gym Hero — 2.81 / 6.0
**Behavior:** Both genre and mood scored zero for every song (songs.csv uses lowercase "pop" and "happy"). The recommender fell back to energy + acousticness + valence only, producing a maximum possible score of 3.0. The actual pop/happy song (Sunrise City) fell to #3 — ironically behind the song that best fits the user's intent — because Gym Hero's energy (0.93) was slightly closer to the 0.85 target than Sunrise City's (0.82).

**Flaw exposed:** Exact string matching with no case normalization. A user typing "Pop" instead of "pop" gets completely different (and wrong) results with no error message.

#### Adversarial 4: Acoustic + High Energy Conflict (energy=0.92, likes_acoustic=True, genre=folk)
**Top result:** Campfire Songs — 5.16 / 6.0
**Behavior:** Campfire Songs is the only folk/introspective song, so it earned 3.0 points (genre + mood) before energy and acousticness ran. Despite its energy (0.45) being far from the target (0.92), the genre+mood lead was insurmountable. Songs #2–#5 were acoustic-heavy non-folk songs like Romantic Strings and Coffee Shop Stories — high acousticness but no genre or mood match.

**Flaw exposed:** The two signals (high energy + likes_acoustic) are fundamentally contradictory — high-energy songs in the catalog have very low acousticness and vice versa. The system never detects or flags this conflict. The explanation says Campfire Songs scored well on acousticness but says nothing about the energy mismatch being a problem.

#### Adversarial 5: Happy Mood, Sad Valence (mood=happy, valence=0.05)
**Top result:** Sunrise City — 5.39 / 6.0
**Behavior:** The contradictory signals barely mattered. Valence is only worth 0.5 pts maximum, so even a near-worst valence score (Sunrise City's valence=0.84 vs. target=0.05 earns only 0.11 pts instead of 0.50) costs less than half a point. Genre + mood + energy + acousticness overwhelmed the valence mismatch. Rankings were essentially unchanged compared to baseline High-Energy Pop.

**Flaw exposed:** Valence at 8% of the total score is too weak to correct for a contradictory user intent. A user asking for happy music but sad tone would see no difference from a normal happy-music request.

#### Adversarial 6: Genre Not in Catalog (genre="k-pop")
**Top result:** Sunrise City — 3.75 / 6.0
**Behavior:** No genre points were earned by any song (k-pop is absent from the catalog). The system returned a ranked list confidently, led by songs that matched the happy mood and high energy/electronic preferences. Sunrise City won on mood match + energy + acousticness alone. The 2.0-point genre weight was simply lost — the effective max score dropped to 4.0 without the user knowing.

**Flaw exposed:** The system confidently returns recommendations even when the user's most important preference (genre) cannot be satisfied at all. A real system would warn: "No songs found for genre 'k-pop'. Showing closest matches by mood and energy instead."

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

