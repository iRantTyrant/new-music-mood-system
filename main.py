#Import the necessary libraries
import os
from src.prediction import get_emotion_predictions
from src.get_mood import get_mood

#Paths to the models and audio files
folder = "data"
vggish_model_path = "models/audioset-vggish-3.pb"
deam_model_path = "models/deam-audioset-vggish-2.pb"

#List all the audio files in the folder
audio_files = [f for f in os.listdir(folder) if f.endswith('.wav')]

#Iterate through each audio file and get the predictions
for audio_file in audio_files:
    for _ in range(2):
        print("\n")
    audio_path = os.path.join(folder, audio_file)
    print(f"Processing {audio_file}...")
    preds = get_emotion_predictions(audio_path, vggish_model_path, deam_model_path)
    print("Mean normalized valence/arousal:", preds["mean_normalized_minus1_1"])
    print("Mean valence/arousal:", preds["mean"])
    valence = preds["mean_normalized_minus1_1"][0]
    arousal = preds["mean_normalized_minus1_1"][1]
    mood = get_mood(valence, arousal)
    print("The musics overall Mood is:", mood)