#Import necessary libraries and functions
import os #For file and directory handling
from src.prediction import get_emotion_predictions #To get the predictions from the models
from src.get_mood import map_valence_arousal_to_mood #To match the predictions to a mood
from src.visualization import (
    add_point_to_visualization, plot_all_points, reset_points,
    add_mean_point, plot_all_mean_points, reset_mean_points
)#To visualize the songs 
from src.dynamic_visualization import process_visualization_for_song#For the dynamic visualization

#Directory paths 
folder = "data" #For the folder that has the songs we want to process
vggish_model_path = "models/audioset-vggish-3.pb" #For the extractor model
deam_model_path = "models/deam-audioset-vggish-2.pb" #For the DEAM predictor model

audio_files = [f for f in os.listdir(folder) if f.endswith('.wav')] #Take all the files that end in .wav (can be changed to what we want)

reset_mean_points()  #Clean the plot that saves the mean valence arousal (1 for each song not the dynamic one)

#Main for that calls the functions once for each song (each iteration of the for loop)
for audio_file in audio_files:

    #Print empty line for visibility
    print("\n\n")

    #Add the path to the current song being processed and print a message
    audio_path = os.path.join(folder, audio_file)
    print(f"Processing: {audio_file}")

    #Get the Valence and Arousal of a song
    preds = get_emotion_predictions(audio_path, vggish_model_path, deam_model_path)

    # 1. Dynamic visualization per song (frame-by-frame)
    process_visualization_for_song(preds, audio_file)

    # 2. Προσθήκη μέσου σημείου στη λίστα για το all-songs plot
    valence_mean = preds["mean_normalized_minus1_1"][0]
    arousal_mean = preds["mean_normalized_minus1_1"][1]
    valence_DEAM = preds["mean"][0]
    arousal_DEAM = preds["mean"][1]
    mood = map_valence_arousal_to_mood(valence_mean, arousal_mean)
    print(f"Mean Valence: {valence_mean:.2f}, Mean Arousal: {arousal_mean:.2f}, Mood: {mood}")
    print(f"DEAM Mean Valence: {valence_DEAM:.2f}, DEAM Mean Arousal: {arousal_DEAM:.2f}")

    add_mean_point(valence_mean, arousal_mean, mood)

# 3. Σχεδίαση ενιαίου plot με τα mean σημεία όλων των τραγουδιών
plot_all_mean_points()

print("\n[INFO] Όλα τα plots δημιουργήθηκαν επιτυχώς!")