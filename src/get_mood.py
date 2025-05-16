def get_mood(valence, arousal):
    if valence >= 0 and arousal >= 0:
        mood = "Happy / Energetic"
    elif valence >= 0 and arousal < 0:
        mood =  "Calm / Relaxed"
    elif valence < 0 and arousal >= 0:
        mood =  "Anxious / Tense"
    elif valence ==0 and arousal == 0:
        mood = "Neutral"
    else:  # valence < 0 and arousal < 0
        mood = "Sad / Depressed"
    return mood
    