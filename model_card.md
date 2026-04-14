# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

A content-based music recommender that matches songs to a listener's genre, mood, and energy preferences using a simple points system.

---

## 2. Intended Use

**What it is for:**
VibeFinder 1.0 is designed for classroom exploration. It shows how a basic scoring algorithm can turn a few preferences into a ranked list of song suggestions. It is a teaching tool, not a product.

**What it tries to do:**
Given a listener's favorite genre, favorite mood, target energy level, and whether they prefer acoustic or electronic sound, it scores every song in the catalog and returns the top five matches.

**What it assumes about the user:**
It assumes the user knows their own preferences and can describe them in exact terms — for example, they know they want "lofi" not just "calm music," and they know their energy target is roughly 0.35 not just "relaxed."

**What it should NOT be used for:**
- Do not use this for real music recommendations. The catalog only has 18 songs.
- Do not use this to make decisions about what music "works" for real people or real moods.
- Do not treat the scores as meaningful percentages or quality ratings.
- Do not deploy this in any product where users expect accurate or personalized results.

---

## 3. How the Model Works

Every song in the catalog gets scored on five things. All the points are added up, and the songs with the most points are recommended first.

**Genre** is worth the most — up to 2 points. If the song's genre matches what the user asked for, they get the full 2 points. If not, they get zero. There is no in-between.

**Mood** works the same way. If the song's mood matches, add 1 point. If not, zero.

**Energy** is scored by closeness. If a user wants high energy (say 0.9 out of 1.0) and a song has energy 0.91, that is almost a perfect match. If the song has energy 0.3, that is far off. The system gives up to 1.5 points based on how close the match is.

**Acousticness** is about direction. If the user likes acoustic music, songs with high acousticness score higher. If the user prefers electronic, songs with low acousticness score higher. Either way, the rule rewards what the user asked for. Up to 1 point.

**Valence** is like energy — it rewards closeness. Valence measures how emotionally positive a song is. This one is only worth 0.5 points, so it mostly acts as a tiebreaker.

The maximum possible score is 6.0 points. A song that matches every single preference perfectly would get a 6.0.

---

## 4. Data

The catalog has **18 songs**. Each song has these fields:

- **Title and artist** — just for display
- **Genre** — the musical category (pop, lofi, rock, jazz, metal, folk, etc.)
- **Mood** — the emotional label (happy, chill, intense, relaxed, focused, etc.)
- **Energy** — a number between 0 and 1 (0 = very calm, 1 = very intense)
- **Tempo** — beats per minute
- **Valence** — a number between 0 and 1 (0 = dark/sad tone, 1 = upbeat/positive)
- **Acousticness** — a number between 0 and 1 (0 = very electronic, 1 = very acoustic)
- **Danceability, instrumentalness, speechiness, liveness, loudness, popularity** — loaded but not used in scoring

**Limits of the data:**
- 13 out of 15 genres appear only once. Most listeners will only ever get one genre match in their entire top 5.
- Only lofi has 3 songs, and only pop has 2. Everyone else gets 1.
- The catalog has no K-pop, Latin, gospel, classical fusion, or regional music.
- All mood and genre labels are lowercase strings. Typing "Pop" instead of "pop" breaks the scoring silently.
- No song was added or removed from the original starter dataset.

---

## 5. Strengths

The system works best when the user's preferred genre and mood both appear in the catalog and more than one song matches.

**Lofi listeners** get the best experience. Three lofi songs exist, all with calm energy and high acousticness. The top three results for a chill lofi profile were all genuinely lofi songs. That feels right.

**Pop and rock listeners** also get a strong #1 result. Sunrise City (pop/happy) and Storm Runner (rock/intense) both scored above 5.7 out of 6.0, which means the algorithm found nearly perfect matches when they existed.

**The scoring is transparent.** Every recommendation comes with a short explanation of why it ranked where it did — genre match, mood match, energy gap, acousticness direction. A user can read it and understand exactly why a song was suggested.

**The formula is symmetric.** A chill user wanting low energy gets the same quality of energy scoring as a high-energy user. Neither side of the dial is penalized more than the other by the math itself.

---

## 6. Limitations and Bias

The most significant bias discovered during testing is what can be called the **single-song genre trap**: 13 out of 15 genres in the catalog have exactly one song, yet genre match carries the largest single weight in the scoring formula (2.0 points, 33% of the total). This means a user who prefers rock, metal, jazz, folk, R&B, or any other minority genre receives their genre bonus on exactly one song, and every remaining recommendation in their top 5 is chosen purely by energy proximity, acousticness, and valence — features that are shared across unrelated genres. In practice, a rock fan's second through fifth recommendations were Gym Hero (pop), Metallic Fury (metal), Electric Surge (electronic), and Bass Rebellion (hip hop) — none of them rock — because the algorithm had no genre signal left to differentiate them after Storm Runner claimed the single rock-match bonus. Lofi listeners, by contrast, benefit from three genre-matching songs in the catalog (17% of songs vs. 6% for most genres), so their top three results are genre-consistent while everyone else's list collapses into a genre-blind energy leaderboard after rank one. This creates an unequal experience where the system works as a genuine genre recommender for lofi and pop fans but effectively ignores genre preference for the majority of user types.

---

## 7. Evaluation

Nine user profiles were tested by running `python -m src.main` against the full 18-song catalog. Three were realistic listener types and six were deliberately broken ("adversarial") profiles designed to see where the system fails.

**Profiles tested:**

1. **High-Energy Pop** — genre=pop, mood=happy, energy=0.90. A straightforward, well-supported profile. The system returned Sunrise City at #1 (5.70/6.0), which felt completely right: it matched genre, mood, and energy simultaneously.

2. **Chill Lofi** — genre=lofi, mood=chill, energy=0.35. Also worked well. Library Rain scored 5.86/6.0 because it hit every signal at once: lofi genre, chill mood, exactly 0.35 energy, and high acousticness (0.86). The top three results were all lofi songs, which is exactly what this listener wants.

3. **Deep Intense Rock** — genre=rock, mood=intense, energy=0.92. Storm Runner scored 5.84/6.0 and was a clear winner. However, positions 2 through 5 were pop, metal, electronic, and hip hop — no more rock songs. After the single rock song was claimed, genre stopped mattering entirely for the rest of the list.

4. **Adversarial — Nonexistent Mood ("sad")** — genre=rock, mood=sad, energy=0.90. "Sad" does not exist in the catalog. The system returned high-energy rock songs with no warning that the mood was never matched. This was surprising: a real user asking for sad music would have no idea the system simply ignored that request.

5. **Adversarial — Out-of-Range Energy (energy=1.5)** — energy above the valid 0–1 scale. Genre and mood bonuses kept the top results reasonable, but all energy scores were artificially low. Songs far from 1.5 actually received negative energy contributions from the formula, which was not obvious from the output.

6. **Adversarial — Case Mismatch (genre="Pop", mood="Happy")** — capitalized inputs that do not match the lowercase values in the CSV. Both genre and mood scored zero for every single song. The best score in the entire run was only 2.81/6.0, and the system never flagged the problem. Sunrise City — the obvious correct answer — fell to #3.

7. **Adversarial — Acoustic + High Energy Conflict** — energy=0.92, likes_acoustic=True. These two preferences point in opposite directions because high-energy songs in the catalog have very low acousticness. Campfire Songs (folk, energy=0.45) still won because it was the only song matching the folk/introspective genre+mood combination, earning 3.0 points before energy even ran. The system had no way to recognize or warn about the internal contradiction.

8. **Adversarial — Happy Mood, Sad Valence (valence=0.05)** — mood=happy but emotional tone target near zero. Surprisingly, the rankings barely changed from the normal happy pop run. Valence only contributes a maximum of 0.5 points, so the severe mismatch cost Sunrise City only 0.31 points compared to baseline. The system effectively ignored the contradictory valence signal.

9. **Adversarial — Genre Not in Catalog ("k-pop")** — genre entirely absent from the dataset. The system returned a confident ranked list with Sunrise City at #1 (3.75/6.0), driven by mood and energy alone. No warning that the most-weighted preference could not be satisfied at all.

**What was most surprising:**

The biggest surprise was how completely invisible the failures are. Every profile — even the six broken ones — received a neatly formatted ranked list with explanations. Nothing in the output tells the user that their mood was never matched, their genre doesn't exist, or their input was outside the valid range. A user reading these results would have no reason to doubt them. The system looks confident even when it has silently thrown away the user's most important preference.

---

## 8. Ideas for Improvement

**1. Fix case sensitivity and missing genre/mood warnings.**
Before scoring anything, convert the user's input to lowercase to match the CSV. If no song in the catalog matches the genre or mood, print a warning like "No songs found for genre 'K-Pop' — showing closest matches by energy and mood instead." This would have fixed three of the six adversarial failures immediately.

**2. Add partial credit for related genres.**
Right now, "pop" and "indie pop" score 0 for a pop fan even though they are closely related. A simple lookup table — where pop gives 2.0 to pop, 0.8 to indie pop, and 0.3 to synthwave — would surface better cross-genre suggestions and reduce the filter bubble. Mood could work the same way: "chill" and "relaxed" are close; "happy" and "euphoric" are close.

**3. Expand the catalog so each genre has at least 3–5 songs.**
The single-song genre trap is a data problem as much as an algorithm problem. With only one rock song, no amount of scoring logic can give a rock fan a genre-consistent top five. Adding 2–4 more songs per genre would make the recommendations feel meaningful past position #1 for most listener types.

---

## 9. Personal Reflection

**What was the biggest learning moment?**
The biggest learning moment was running the adversarial profiles and seeing that the system always returned a confident, clean-looking result — even when the input was completely broken. I had assumed that a wrong input would produce a visibly wrong output. Instead, it produced a normal-looking list with reasonable-sounding explanations. That gap between "the output looks fine" and "the output is actually wrong" is one of the most important things to understand about AI systems. You cannot trust the presentation of a result to tell you whether the result is good.

**How did using AI tools help, and when did you need to double-check them?**
AI tools were helpful for exploring the codebase quickly and for running multiple experiments without having to manually rewrite the code each time. They also helped with drafting explanations for complex scoring behavior. But I had to double-check any claim about specific scores or rankings — the model would sometimes describe a result confidently that did not match what the actual Python output said. The rule I developed was: always run the code and read the numbers before writing anything as fact.

**What surprised you about how simple algorithms can still "feel" like recommendations?**
The most surprising thing is how much the formatting does the work. When the output says "#1 Sunrise City — Score: 5.70 / 6.0 — genre match, mood match, energy 0.82," it feels like the system truly understood what you wanted. But the underlying logic is just five arithmetic rules that add points. There is no understanding at all. The explanation text makes it feel smart even when the system is silently ignoring half the user's request. Real recommendation systems at Spotify or YouTube are far more complex, but this project showed that even a very simple formula can produce output that feels personalized and thoughtful.

**What would you try next if you extended this project?**
The first thing I would add is a warning system — any time a genre, mood, or other key preference cannot be matched, tell the user explicitly instead of silently scoring zero. After that, I would expand the catalog to at least 5 songs per genre so the recommendations stay genre-consistent past position #1. Finally, I would try adding a collaborative filter on top of the content-based one: instead of only comparing features, also track which songs users actually listened to after receiving a recommendation and use that signal to adjust future scores. That is closer to how real apps work, and it would be interesting to see how much the rankings change when real listening behavior is included.
