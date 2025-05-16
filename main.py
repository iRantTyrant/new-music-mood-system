import os
from src.prediction import get_emotion_predictions
from src.get_mood import map_valence_arousal_to_mood
from src.visualization import (
    add_point_to_visualization, plot_all_points, reset_points,
    add_mean_point, plot_all_mean_points, reset_mean_points
)
from src.dynamic_visualization import process_visualization_for_song

folder = "data"
vggish_model_path = "models/audioset-vggish-3.pb"
deam_model_path = "models/deam-audioset-vggish-2.pb"

audio_files = [f for f in os.listdir(folder) if f.endswith('.wav')]

reset_mean_points()  # Καθαρίζουμε τη λίστα με τα mean points

for audio_file in audio_files:
    print("\n\n")
    audio_path = os.path.join(folder, audio_file)
    print(f"Processing: {audio_file}")

    preds = get_emotion_predictions(audio_path, vggish_model_path, deam_model_path)

    # 1. Dynamic visualization per song (frame-by-frame)
    process_visualization_for_song(preds, audio_file)

    # 2. Προσθήκη μέσου σημείου στη λίστα για το all-songs plot
    valence_mean = preds["mean_normalized_minus1_1"][0]
    arousal_mean = preds["mean_normalized_minus1_1"][1]
    mood = map_valence_arousal_to_mood(valence_mean, arousal_mean)
    print(f"Mean Valence: {valence_mean:.2f}, Mean Arousal: {arousal_mean:.2f}, Mood: {mood}")

    add_mean_point(valence_mean, arousal_mean, mood)

# 3. Σχεδίαση ενιαίου plot με τα mean σημεία όλων των τραγουδιών
plot_all_mean_points()

print("\n[INFO] Όλα τα plots δημιουργήθηκαν επιτυχώς!")