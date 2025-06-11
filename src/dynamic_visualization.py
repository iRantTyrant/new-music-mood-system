#Import necessary functions
from src.visualization import add_point_to_visualization, plot_all_points, reset_points #For the visualization
from src.get_mood import map_valence_arousal_to_mood #To match the mood to a colour
from src.mpeg_creation import create_dynamic_animation #To create the trace animation
from src.utils import slugify
import os #For file and directory handling
import json #For saving the metadata of the song


#The actual function 
def process_visualization_for_song(preds, audio_file_name,threshold):
    """
    Παίρνει όλα τα valence/arousal frames και φτιάχνει scatter plot.
    """
    #Take the values for the valences and arousals of the song (almost every 1 second)
    valences = preds["predictions_normalized_minus1_1"][:, 0]
    arousals = preds["predictions_normalized_minus1_1"][:, 1]

    #Delete last song plot
    reset_points()

    #For loop that for each iteration it maps the valence arousal to a mood gets it's colour and adds it to the plot
    for val, ar in zip(valences, arousals):
        mood = map_valence_arousal_to_mood(val, ar,threshold)
        add_point_to_visualization(val, ar, mood)

    #Create a directory for each song based on the slugifyied name 
    song_slug = slugify(audio_file_name)
    song_output_dir = os.path.join("output", song_slug)
    os.makedirs(song_output_dir, exist_ok=True)

    #Save the plot of the song
    plot_all_points("mood_plot", output_dir=song_output_dir)

    #The function that creates a snake like trace animation
    create_dynamic_animation(audio_file_name, output_dir=song_output_dir, frame_interval_sec=0.5)

    #JSON metadata for the song
    median_valence = preds["median_normalized_minus1_1"][0]
    median_arousal = preds["median_normalized_minus1_1"][1]
    mood = map_valence_arousal_to_mood(median_valence, median_arousal,threshold)

    with open(os.path.join(song_output_dir, "metadata.json"), "w") as f:
        json.dump({
            "title": audio_file_name,
            "valence": median_valence,
            "arousal": median_arousal,
            "mood": mood
        }, f, indent=2)