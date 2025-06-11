import math
import numpy as np

def compute_adaptive_threshold(points):
    distances = [math.sqrt(v**2 + a**2) for v, a, _ in points]
    median_distance = np.median(distances)
    threshold = max(median_distance * 0.8, 0.05)  
    print(f"Median distance: {median_distance}, Adaptive threshold: {threshold}")
    return threshold

def map_valence_arousal_to_mood(valence, arousal, threshold):
    distance = math.sqrt(valence**2 + arousal**2)
    if distance < threshold:
        return "Neutral / Ambiguous"
    
    angle = math.degrees(math.atan2(arousal, valence))
    print(f"Computed angle: {angle} degrees", f"with valence: {valence}, arousal: {arousal}, threshold: {threshold},distance: {distance}")
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
    else:
        return "Sorrowful"
