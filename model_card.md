# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**  

---

## 2. Intended Use  

 VibeMatch takes one person's stated music taste (favorite genre, favorite mood, and target energy level) and picks the top songs from a small catalog that best match that taste. It assumes the user already knows what genre, mood, and energy they want and can describe it in simple terms, it does not try to guess taste from listening history or behavior. This is a classroom project meant to demonstrate how a basic content-based recommender works, not a production system for real listeners.

**Intended use:** learning and demonstrating how content-based scoring and ranking work, on a small, known catalog, for a single stated user profile at a time.

**Not intended for:** real-world music recommendations at scale, personalizing based on real listening history, making claims about "what people like me listen to" (it has no notion of other users), or any use where a biased or repetitive recommendation could cause real harm (for example, this should not be used to make decisions about a real product's catalog without much more testing and a much bigger, more balanced dataset).

---

## 3. How the Model Works  
Each song has a genre, a mood, and an energy level (how intense or calm it feels, from 0 to 1). The user tells the system their favorite genre, favorite mood, and target energy level. For every song, the system hands out points: +2 points if the genre matches exactly, +1 point if the mood matches exactly, and up to +1 point for energy, where the closer the song's energy is to what the user wants, the more points it gets. All the points get added up into one score per song, and the songs with the highest scores are shown first, along with a plain-language reason for each point they earned. The starter file only had empty placeholder functions, so I designed and built this whole point system myself, decided how much each feature should count, and made sure every recommendation comes with an explanation instead of just a bare list of songs.

---

## 4. Data  

The catalog has 18 songs total. I started with 10 (covering pop, lofi, rock, ambient, jazz, synthwave, and indie pop) and added 8 more to cover genres and moods that weren't represented yet: hip hop, folk, R&B, metal, country, electronic, reggae, and classical, paired with moods like triumphant, nostalgic, romantic, angry, melancholic, euphoric, and dreamy. Even after adding those, most genres only have 1-2 songs each, so the dataset is still tiny and lopsided compared to a real streaming catalog. It's also missing a lot of real musical taste: there's no way to express liking a specific artist, decade, language, instrument, or lyrical theme, and every song only has one genre and one mood label even though real songs often blend several.

---

## 5. Strengths 

The system works well for users whose favorite genre already has several songs in the catalog, like pop or lofi fans. For those users, the top recommendation is almost always a genuinely great match on genre, mood, and energy all at once, and the explanations correctly describe why ("genre match," "mood match," "energy similarity"). It also correctly tells apart very different users: a chill lofi listener and an intense rock listener get completely different, non-overlapping top picks, which matches what a person would expect. The scoring also correctly rewards "close but not exact" energy matches instead of only rewarding perfect matches, which feels more realistic than an all-or-nothing rule.

---

## 6. Limitations and Bias 

During testing, I found that the system structurally favors users whose favorite genre is well-represented in the catalog, like `pop` or `lofi`, which each have several songs. Because genre match is worth double the points of mood match (+2.0 vs +1.0) and there is no diversity mechanism, users who like a well-covered genre get several strong, well-rounded matches, while users who prefer a genre with only one or two songs in the catalog (like `metal`, `classical`, or `reggae`) get one decent match and then a "top 5" filled with songs that don't actually match their genre or mood at all, just whatever happens to have similar energy. This means the quality of recommendations a user receives depends heavily on how popular their taste happens to be in the dataset, not just on how well the algorithm works, which is a small-scale example of the same popularity bias that can show up in real-world recommenders. I also noticed that `likes_acoustic` is stored in the `UserProfile` but never actually used in scoring, so a user's stated acoustic preference currently has zero effect on their results even though the system implies it's being considered.

---

## 7. Evaluation  


I tested three profiles side by side (see `src/main.py`): **High-Energy Pop** (`genre=pop, mood=happy, energy=0.8`), **Chill Lofi** (`genre=lofi, mood=chill, energy=0.35`), and **Deep Intense Rock** (`genre=rock, mood=intense, energy=0.9`). For each one, I checked whether the #1 recommendation was actually a song that shares that genre and mood, and whether the rest of the list still made sense even if it didn't get a perfect match.

**Comparing High-Energy Pop vs. Chill Lofi:** These two profiles want almost opposite things, one wants upbeat, happy, high-energy music, the other wants calm, low-energy background music. The output reflected that correctly: the Pop profile's top pick was "Sunrise City" (happy pop, high energy), while the Lofi profile's top pick was "Library Rain" (chill lofi, low energy). This makes sense because the two profiles don't overlap at all on genre, mood, or energy, so the system had no trouble telling them apart.

**Comparing Chill Lofi vs. Deep Intense Rock:** Same story here, Lofi wants low energy and a relaxed feel, Rock wants very high energy and intensity, so their top picks ("Library Rain" vs. "Storm Runner") landed on opposite ends of the catalog. This is the clearest, most "obviously correct" comparison, since every feature (genre, mood, and energy) pulls in a different direction for these two.

**Comparing High-Energy Pop vs. Deep Intense Rock:** This is the pair that surprised me. Even though "pop, happy" and "rock, intense" are different genres and different moods, they share one thing: both profiles want high energy (0.8 and 0.9). Because of that overlap, "Gym Hero" (a high-energy pop song, energy=0.93) showed up in the top 5 for *both* profiles, it landed at #2 for High-Energy Pop (genre + energy match) and also at #2 for Deep Intense Rock (mood mismatch, but a very close energy match). In plain terms: "Gym Hero" is basically a pop song that "sounds" intense because it's loud and fast, so a system that leans heavily on the *energy number* instead of genre or mood can end up recommending the same high-energy song to someone who wants a happy pop workout song and someone who wants angry, intense rock music, even though a person would say those are pretty different vibes. It's a good example of the system sometimes confusing "sounds similarly intense" with "is actually the right style of music."

---

## 8. Future Work  

1. Actually use `likes_acoustic` in the score instead of just storing it, and add valence/danceability as optional bonus features for users who care about them. 2. Add a diversity rule so the top 5 isn't allowed to be dominated by one genre, so users occasionally get a well-matched song from a genre they haven't tried yet instead of just more of the same. 3. Let genre and mood matching be a little "fuzzy" (case-insensitive, and maybe allow related genres to get partial credit) instead of requiring an exact text match, so small labeling differences don't quietly zero out a user's score.

---

## 9. Personal Reflection  

My biggest learning moment was realizing that recommender systems are basically just big math problems. Everything gets turned into a number on some scale, and those numbers are what actually decide your next swipe, listen, or watch. Building VibeMatch made that concrete for me: genre, mood, and energy are just fields in a dataclass, and "does this song fit you" boils down to adding up a few points and sorting a list. What surprised me is how much depth real systems add on top of that same basic idea. I hadn't thought about how something like watch time on a video gets folded into that scoring the same way genre or mood does here.

Using an AI assistant helped me move fast on the parts I already understood conceptually but hadn't coded before, like using Python's `csv` module correctly or writing the sorting/ranking logic. It also pushed me to think harder about bias by pointing out things I wouldn't have caught on my own, like the fact that `likes_acoustic` was sitting unused in my `UserProfile`, or that giving genre 2x the weight of mood could quietly favor users whose taste matched the most common genres in my catalog. I had to double-check anything it suggested about scoring weights or "what the data shows," since those are judgment calls, not facts, I made sure the example outputs and score numbers it referenced were things I could actually reproduce myself by running the code, rather than trusting them at face value.

What surprised me most is how "smart" a system this simple can feel. Even a handful of if-statements and one distance formula produce a top-5 list that feels personal and reasonable, as long as the explanations ("genre match," "energy similarity") are shown alongside it. That makes me trust real recommendation apps less, not more, since it shows how a system can look and feel thoughtful while actually running on a fairly small set of rules and a lot of data about you. If I extended this project, I'd want to try using real weighted preferences instead of exact-match genre/mood, add a diversity rule so recommendations don't all pile into one genre, and actually wire up `likes_acoustic` and other unused features so nothing a user tells the system just gets silently ignored.
