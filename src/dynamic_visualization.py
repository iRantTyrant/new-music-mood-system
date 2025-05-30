#Import necessary functions
from src.visualization import add_point_to_visualization, plot_all_points, reset_points #For the visualization
from src.get_mood import map_valence_arousal_to_mood #To match the mood to a colour
from src.mpeg_creation import create_dynamic_video #To create the trace animation

#The actual function 
def process_visualization_for_song(preds, audio_file_name):
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
        mood = map_valence_arousal_to_mood(val, ar)
        add_point_to_visualization(val, ar, mood)

    #We plot all the points of the song 
    plot_all_points(audio_file_name + "'s Dynamic Visualization")

    #The function that creates a snake like trace animation
    create_dynamic_video(audio_file_name, frame_interval_sec=0.5)