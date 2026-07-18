# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**Bruce's VibeFinder 1.0**

A small content-based music recommender that scores songs against a user's taste profile and returns the best matches ranked by total score.

---

## 2. Intended Use

VibeFinder 1.0 is designed for **classroom exploration** — specifically to understand how a content-based recommendation algorithm works step by step.

It is meant for:
- Students and developers learning how recommender systems turn data into ranked lists
- Experimenting with how changing feature weights changes the output
- Exploring what "bias" and "filter bubbles" mean in a concrete, hands-on setting

It assumes the user already knows what genre, mood, and energy level they prefer, and that those preferences can be expressed as a simple dictionary.

**This system is NOT intended for:**
- Real music streaming platforms with millions of songs — the scoring logic is too simple and the catalog too small to generalize
- Users who have not provided a preference profile — the system has no way to learn from listening history
- Situations where fairness across genres or cultures is important — underrepresented genres will always get fewer matches

---

## 3. How the Model Works

Imagine you walk into a record store and tell the clerk: *"I like Rock, I want something Intense, and I want it to feel high-energy."* The clerk then goes through every record in the store, gives each one a score, and hands you the top five.

VibeFinder 1.0 works exactly like that clerk, using three rules:

**Rule 1 — Genre match (+1.0 point):**
If a song's genre label exactly matches what the user asked for, it gets 1 point. No partial credit — either it matches or it doesn't.

**Rule 2 — Mood match (+1.0 point):**
Same idea. If the mood tag on the song matches the user's preferred mood, it gets 1 point.

**Rule 3 — Energy proximity (up to +2.0 points):**
This is the most interesting rule. Instead of just asking "is the energy right or wrong?", it uses a bell-curve formula to reward closeness. A song with energy almost exactly matching the user's target gets close to 2.0 points. A song that's a little off gets maybe 1.5. A song that's way off gets nearly 0. The closer, the better — but there's no hard cutoff.

The three scores are added together (maximum possible: 4.0 points), and all songs are ranked from highest to lowest. The top K songs are returned as recommendations.

At every step, the system also records *why* each point was awarded, so the output tells you: "Genre match (+1.0) | Energy match (+1.84)" — not just a number.

---

## 4. Data

The catalog is **songs.csv**, a hand-curated dataset of **10 songs** built for testing and exploration.

Each song has the following attributes:
- **title** and **artist** — for display
- **genre** — one of: pop, lofi, rock, ambient, jazz, synthwave, indie pop
- **mood** — one of: happy, chill, intense, moody, relaxed, focused
- **energy** — a decimal between 0.0 (completely calm) and 1.0 (maximum intensity)
- **tempo_bpm** — beats per minute
- **valence** — emotional positivity (0.0 = dark/sad, 1.0 = bright/happy)
- **danceability** and **acousticness** — additional texture features

**What is missing from this dataset:**
- Only 10 songs — a real platform has tens of millions
- Genre coverage is uneven: lofi has 3 songs (30%), while jazz, rock, synthwave, and indie pop each have only 1
- No songs in Spanish, Mandarin, or other non-English languages
- No classical music, hip-hop, R&B, country, or metal
- No user listening history — every recommendation starts from scratch
- Tempo, valence, danceability, and acousticness are recorded but not yet used in scoring

---

## 5. Strengths

VibeFinder 1.0 works best for users with **clear, specific preferences** that happen to match common genre/mood combinations in the catalog.

- A user who says `genre: lofi, mood: chill, energy: 0.38` will consistently receive reasonable and relevant results, because three lofi songs exist and their energy values cluster near that range
- The energy Gaussian produces naturally graded results — it does not feel like a binary pass/fail, and songs that are "close enough" still appear rather than being completely excluded
- The reasons list makes the system transparent and easy to debug: you can always see exactly why a song ranked where it did
- The system responds predictably to weight changes — halving the genre weight and doubling the energy weight measurably shifted which songs ranked first, exactly as expected from the math

---

## 6. Limitations and Bias

**Exact-string genre matching creates invisible walls.**
"indie pop" and "pop" score zero against each other, even though a pop fan would almost certainly enjoy an indie pop song. The system has no concept of genre proximity — every non-matching genre is treated as equally wrong, whether it's "indie pop" (very close) or "ambient" (very far).

**lofi songs dominate the catalog.**
30% of songs are lofi, and all three lofi songs share the mood "chill." A lofi/chill user gets genre and mood bonuses on multiple songs, producing a narrowly similar top-3. A jazz user gets genre bonus on only one song. This is a catalog representation bias that unfairly advantages common genres.

**Mood labels have no gradient.**
"chill" and "relaxed" score zero against each other even though they describe almost the same feeling. Meanwhile, the energy Gaussian rewards small differences smoothly. The two features operate at completely different levels of precision, which distorts the ranking.

**No listening history means no personalization over time.**
Every session starts from a manually typed profile. A real recommender learns what you actually skip, replay, and save. This system cannot do that.

**The system can recommend near-duplicate songs.**
There is no diversity rule. If three songs all score very similarly, all three appear in the top-3 — even if they sound nearly identical. A real system would enforce variety across the final list.

---

## 7. Evaluation

Four user profiles were tested to stress-test the scoring logic:

**Standard profile** (`genre: rock, mood: intense, energy: 0.85`):
Storm Runner ranked first with a score near 3.0 — genre and mood both matched, and its energy of 0.91 was close to the target. This matched intuition perfectly.

**The Contradiction** (`genre: blues, mood: melancholic, energy: 0.92`):
The only blues song in the catalog has energy 0.33 — completely opposite of the target. But the genre match alone pushed it to first place. This confirmed the genre over-prioritization bias: a song can "win" purely on its label even when every sonic feature is wrong.

**The Ghost Genre** (`genre: K-Pop, mood: euphoric, energy: 0.75`):
Since no K-Pop songs exist in the catalog, the +1.0 genre bonus never fired for any song. The recommender silently became a mood + energy-only system, and still returned a reasonable result (Oye Como Va ranked first based on mood match and close energy). This showed that the system degrades gracefully when genre is missing.

**The Genre Trap** (`genre: rock, mood: serene, energy: 0.05`):
After changing energy weight to ×2.0, Spacewalk Thoughts (ambient, chill, energy 0.28) correctly beat Storm Runner (rock, intense, energy 0.91) — the near-perfect energy match finally outweighed the genre label. Before the weight change, the rock song had won despite being the exact opposite of what the user wanted sonically.

---

## 8. Future Work

**Add a diversity rule to the ranking step.**
Currently the top-K list can contain very similar songs. A simple fix would be: after scoring all songs, remove any song whose energy is within 0.05 of a higher-ranked song already in the results. This would force the list to cover a broader range.

**Replace exact mood matching with a valence score.**
Instead of matching the string "chill" to "chill," convert moods to a number on the happy-to-sad scale (valence). Then apply the same Gaussian formula used for energy. "Relaxed" and "chill" would score nearly identically, while "intense" and "serene" would score nearly zero against each other — a much more realistic model of how moods relate.

**Add a decade or era feature.**
A user who loves 90s music would want songs from that era boosted. Adding a `year` column and a small bonus for era-matching would let the system distinguish between a classic rock fan and a modern indie fan, even if both select `genre: rock`.

**Expand the catalog with at least 50 songs across 10+ genres.**
The current 10-song, 7-genre catalog is too small for the scoring differences to be meaningful. With more songs, the Gaussian decay becomes a genuine differentiator rather than a tiebreaker.

---

## 9. Personal Reflection

**Biggest learning moment:**
The moment that stuck most was discovering that a genre match worth +1.0 (or +2.0 in the original design) can mathematically overpower a near-perfect energy match. Before running the numbers, it seemed obvious that "energy is important" — but seeing *Storm Runner* beat *Spacewalk Thoughts* by just 0.02 points when the user wanted serene, low-energy music made the bias concrete in a way that a theoretical explanation could not. The math made the unfairness visible.

**How AI tools helped, and when to double-check:**
Claude helped move quickly through designing the scoring formula, generating test data, and writing the load_songs and score_song functions. But the process also required careful checking — for example, the import path in main.py was `from recommender import ...` in the original but needed to become `from src.recommender import ...` when running from the project root. AI-generated code needs to be read, not just run, because it is optimized for the described context, not the actual filesystem layout.

**Surprise about simple algorithms:**
What was genuinely surprising is how much "recommendation feeling" comes from the reasons list, not the score itself. A number like 2.76 is meaningless. But "Genre match (+1.0) | Mood match (+1.0) | Energy match (+0.76)" feels like an explanation a real music app might give. The experience of receiving a recommendation is shaped as much by transparency and language as by the underlying math.

**What to try next:**
The most interesting next step would be adding user feedback — if a user skips a recommended song, reduce the weight of the feature that drove that recommendation. After ten sessions, the profile would adapt automatically rather than requiring the user to manually update a dictionary. That gap between "static preferences" and "learned preferences" is the real difference between this simulation and a production recommender.
