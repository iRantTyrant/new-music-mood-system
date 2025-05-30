import math

"""
Converts valence and arousal to a mood label using Russell's Circumplex Model of Affect.

Parameters:
- valence (float): Emotional valence [-1, 1]
- arousal (float): Emotional arousal [-1, 1]

Returns:
- str: Mood label
"""

def map_valence_arousal_to_mood(valence, arousal):
    distance = math.sqrt(valence**2 + arousal**2)
    if distance < 0.05:
        return "Neutral / Ambiguous"

    angle = math.degrees(math.atan2(arousal, valence))
    if angle < 0:
        angle += 360

    if 0 <= angle < 30:
        return "Pleasant"
    elif 30 <= angle < 60:
        return "Happy"
    elif 60 <= angle < 90:
        return "Aroused"
    elif 90 <= angle < 120:
        return "Angry"
    elif 120 <= angle < 150:
        return "Frustrated"
    elif 150 <= angle < 180:
        return "Sad"
    elif 180 <= angle < 210:
        return "Depressed"
    elif 210 <= angle < 240:
        return "Slightly Sad"
    elif 240 <= angle < 270:
        return "Calm"
    elif 270 <= angle < 300:
        return "Relaxed"
    elif 300 <= angle < 330:
        return "Content"
    else:  # 330 <= angle < 360
        return "Sorrowful"
