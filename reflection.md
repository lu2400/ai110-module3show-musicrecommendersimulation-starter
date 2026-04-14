# reflection: comparing user profile outputs

---

## pair 1: high-energy pop vs. chill lofi study session

these two profiles are complete opposites. high-energy pop wants loud, fast, happy pop (energy 0.9). chill lofi wants quiet, relaxed tracks with acoustic instruments (energy 0.35).
the results split cleanly. pop got dance-friendly songs like sunrise city and levitating. lofi got quiet tracks like library rain (100/100) and midnight coding.
this makes sense. energy, mood, and genre all point in opposite directions. the acoustic bonus also pulled in spacewalk thoughts even though it is not lofi, because mood and acousticness together were enough to rank it.

---

## pair 2: high-energy pop vs. intense rock workout

both want high energy but differ on genre (pop vs. rock) and mood (happy vs. intense).
rock correctly surfaced storm runner and purple haze. pop got sunrise city and levitating. expected.
the difference is gym hero. it ranked #4 for pop and #3 for rock. for pop it got in via genre match and high energy even though the mood is wrong. for rock it got in via mood match even though the genre is pop, not rock. this shows mood and genre can each push a song into the top 5 on their own.

---

## pair 3: intense rock workout vs. edge: contradictory (high energy + acoustic folk)

both want high energy (0.95 and 0.9). but the contradictory profile also wants folk, melancholic, and acoustic.
rock got high-energy results throughout. the contradictory profile's #1 was harvest moon at energy 0.38.
why? folk genre (+15), melancholic mood (+40), and acoustic (+5) totalled 60 points before energy was even counted. energy added only 19 more. 79 total still beat everything else.
the user wanted energetic folk. it just picked the cluster that scored highest and ignored the rest.

---

## pair 4: high-energy pop vs. edge: ghost genre (country not in catalog)

both want a happy mood. but ghost genre asks for country, which is not in the catalog.
pop got genre bonuses on top of mood matches, pushing scores into the 90s. ghost genre could never earn a genre bonus, so scores stayed in the 80s.
the results were still reasonable. mood carried the recommendations even when genre was useless. a country fan who wants happy music still gets happy music, just not country.

---

## pair 5: edge: ghost genre vs. edge: mood not in catalog (sad/pop)

both edge cases have one missing preference, but they fail differently.
ghost genre worked out fine because "happy" is well represented in the catalog. mood stepped in when genre failed.
sad mood did not work out. no song has mood "sad," so the +40 mood bonus was never awarded. the system fell back to genre and energy. the top result was good as hell by lizzo which is an uplifting anthem. second and third were bright, danceable pop songs.
the user wanted sad music and got the opposite. the system did not warn them or adjust. it just quietly gave them the wrong emotional tone.

---

## pair 6: edge: mood not in catalog vs. edge: contradictory

both fail, but differently.
sad mood fails because the label is missing entirely. the system substitutes energy and genre, which are the wrong signals for emotional matching.
contradictory fails because the user's own preferences conflict. the catalog has folk/melancholic songs and high-energy songs the system picks one cluster and ignores the other.
sad mood gives results that match none of the user's emotional criteria. contradictory at least gives harvest moon, which matches folk and melancholic — two real preferences. contradictory is a more honest failure.

---

## why does gym hero keep showing up?

gym hero is a pop song, mood "intense," energy 0.93. it appeared in the top 5 for four different profiles, including profiles that wanted happy, sad, or melancholic music.
energy proximity is worth up to 40 points, same as a mood match. so if a user wants high energy and gym hero is close, it earns ~38-39 points automatically, no matter what the mood says. add a genre match for pop profiles and it easily scores 53+, which is enough for the top 5.
imagine you told a friend you want happy pop music. they hand you a playlist with a song called gym hero (driving beat, pump-up feel, workout montage energy). you didn't ask for that. but they scored it highly because it was fast, loud, and pop. that is what this recommender does. it does not know "intense" feels different from "happy." it only sees numbers.
