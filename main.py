#Import necessary libraries and functions
import os #For file and directory handling
from src.prediction import get_emotion_predictions #To get the predictions from the models
from src.get_mood import map_valence_arousal_to_mood,compute_adaptive_threshold #To match the predictions to a mood
from src.visualization import (
    add_point_to_visualization, plot_all_points, reset_points,
    add_median_point, plot_all_median_points, reset_median_points , _points
)#To visualize the songs 
from src.dynamic_visualization import process_visualization_for_song#For the dynamic visualization

#Directory paths 
folder = "data" #For the folder that has the songs we want to process
vggish_model_path = "models/audioset-vggish-3.pb" #For the extractor model
deam_model_path = "models/deam-audioset-vggish-2.pb" #For the DEAM predictor model

audio_files = [f for f in os.listdir(folder) if f.endswith('.wav')] #Take all the files that end in .wav (can be changed to what we want)

reset_median_points()  #Clean the plot that saves the median valence arousal (1 for each song not the dynamic one)

#Main for that calls the functions once for each song (each iteration of the for loop)
for audio_file in audio_files:

    #Print empty line for visibility
    print("\n\n")

    #Add the path to the current song being processed and print a message
    audio_path = os.path.join(folder, audio_file)
    print(f"Processing: {audio_file}")

    #Get the Valence and Arousal of a song
    preds = get_emotion_predictions(audio_path, vggish_model_path, deam_model_path)

    # Δημιουργούμε λίστα points για threshold (valence, arousal, mood=None)
    points_for_threshold = [(val, ar, None) for val, ar in preds["predictions_normalized_minus1_1"]]

    # Compute adaptive threshold based on all points
    threshold = compute_adaptive_threshold(points_for_threshold)

    # 1. Dynamic visualization per song (frame-by-frame)
    process_visualization_for_song(preds, audio_file,threshold)

    # 2. Προσθήκη μέσου σημείου στη λίστα για το all-songs plot
    valence_median = preds["median_normalized_minus1_1"][0]
    arousal_median = preds["median_normalized_minus1_1"][1]
    valence_DEAM = preds["median"][0]
    arousal_DEAM = preds["median"][1]

    mood = map_valence_arousal_to_mood(valence_median, arousal_median, threshold)

    print(f"Median Valence: {valence_median:.2f}, Median Arousal: {arousal_median:.2f}, Mood: {mood}")
    print(f"DEAM Median Valence: {valence_DEAM:.2f}, DEAM Median Arousal: {arousal_DEAM:.2f}")

    add_median_point(valence_median, arousal_median, mood)

# 3. Σχεδίαση ενιαίου plot με τα median σημεία όλων των τραγουδιών
plot_all_median_points()

print("\n[INFO] Όλα τα plots δημιουργήθηκαν επιτυχώς!")