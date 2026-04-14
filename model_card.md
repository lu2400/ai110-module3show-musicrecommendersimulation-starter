# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

vibefinder 1.0

---

## 2. Intended Use  

vibefinder 1.0 suggests up to 5 songs from a small 18-song catalog based on a user's preferred genre, mood, and energy level. it assumes the user knows what they want and can describe it with a single genre and mood. it does not learn over time or adapt to listening history.
it is not designed for real streaming platforms or real users.
not intended for: personalised music discovery at scale, users with complex or mixed tastes, or any production use.

---

## 3. How the Model Works  

each song gets a score out of 100. the model checks four things:
does the genre match exactly? if yes, +15 points
does the mood match exactly? if yes, +40 points
how close is the song's energy to what the user wants? up to +40 points closer energy means more points
bonus points if the user likes acoustic music and the song is highly acoustic (+5), or if mood matched and the song has high valence (+3) or high danceability (+2)

mood gets the most weight because vibe matters more than genre when picking what to listen to. energy is a sliding scale so near-matches still earn something. the top 5 scores are returned.

---

## 4. Data  

the catalog has 18 songs. each one stores: title, artist, genre, mood, energy (0–1), tempo in bpm, valence (0–1), danceability (0–1), and acousticness (0–1).
genres in the catalog: pop, lofi, rock, hip-hop, folk, jazz, ambient, synthwave, indie pop, indie rock, alternative rock.
moods in the catalog: happy, chill, intense, relaxed, moody, focused, energetic, uplifting, melancholic.
notable gaps: no country, r&b, classical, or electronic genres. no "sad" mood exists. the catalog was curated by hand for this simulation and does not reflect a balanced sample of real music taste.

---

## 5. Strengths  

the system works well when the user's preferences match common catalog items. a chill lofi user with acoustic preferences got a perfect 100/100 score. rock and pop profiles returned results that felt right; correct genre, correct energy.
the scoring is transparent. every recommendation includes an explanation of exactly what matched. this makes it easy to understand why a song appeared, which is unusual in real recommender systems.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

energy proximity heavily penalises songs that don't exactly match the user's target energy level. high-energy users consistently get only high-energy tracks. this creates a filter bubble — songs with a different energy never get a chance, even if they match in other ways. real users might want variety, but the system assumes they always want the closest energy match.  

---

## 7. Evaluation  

six user profiles were tested by running the recommender against the full 18-song catalog and inspecting the top-5 results for each.

**profiles tested:**

| profile | genre | mood | energy | acoustic |
| --- | --- | --- | --- | --- |
| high-energy pop | pop | happy | 0.9 | no |
| chill lofi study session | lofi | chill | 0.35 | yes |
| intense rock workout | rock | intense | 0.95 | no |
| edge: ghost genre (country not in catalog) | country | happy | 0.7 | no |
| edge: mood not in catalog (sad) | pop | sad | 0.8 | no |
| edge: contradictory (high energy + acoustic folk) | folk | melancholic | 0.9 | yes |

**what i looked for:**

- whether genre and mood matches appeared in the top results  
- how the system handled preferences that had no exact match in the catalog  

**what the results showed:**

the three normal profiles (pop, lofi, rock) all produced good top results
the lofi profile achieved a perfect 100/100 score for library rain, which exactly matched genre, mood, energy, and acousticness
the rock profile correctly surfaced storm runner and purple haze ahead of anything else

**what surprised me:**

gym hero kept appearing for profiles that never asked for intense music. energy proximity scores up to 40 points so a high-energy song can rank in the top 5 even with the wrong mood.
the ghost genre (country) profile fell back to mood matching cleanly. no genre bonus was possible, but the top results were still reasonable happy songs.
the sad mood profile was the weakest. no song in the catalog has mood "sad," so the mood bonus was never awarded. the system defaulted to energy and genre, returning uplifting pop songs to a user who wanted something somber.
the contradictory profile (high energy + folk/melancholic/acoustic) quietly prioritized genre and mood over energy. harvest moon ranked 1 despite its low energy (0.38) because genre + mood + acoustic alone totaled 60 points. the user asked for energetic music and got a quiet folk ballad.

---

## 8. Future Work  

1. treat mood as a hard filter. right now a song with the wrong mood can still rank high if its energy is close enough. this causes gym hero to appear for users who wanted calm or sad music.
2. add partial mood matching. "chill" and "focused" are different labels but feel similar. the system gives zero points for near-miss moods. a simple similarity map would fix this.
3. improve diversity. the top 5 results can all be nearly identical in genre and energy. forcing at least one result from a different genre or mood would give users more variety.

---

## 9. Personal Reflection  

biggest learning moment: mood and energy are both worth up to 40 points. that means the system cannot tell a happy song from an intense one when both are high energy. i did not realise this until gym hero kept showing up everywhere.
ai tools helped me draft the scoring logic and write explanations quickly. i had to double-check the point values, an earlier draft had +30 for genre but the code said +15. that reminded me to always verify against the actual code, not just the summary.
the most surprising thing: the system feels like a real recommender when it works. library rain scoring 100/100 is genuinely satisfying. but it breaks in ways a human listener never would, like giving a sad user uplifting pop songs because the mood label just does not exist in the catalog.
next i would add a mood similarity table so that close moods earn partial points instead of zero.  
