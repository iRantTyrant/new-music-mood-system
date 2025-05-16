from src.visualization import add_point_to_visualization, plot_all_points, reset_points
from src.get_mood import map_valence_arousal_to_mood

def process_visualization_for_song(preds, audio_file_name):
    """
    Παίρνει όλα τα valence/arousal frames και φτιάχνει scatter plot.
    """
    valences = preds["predictions_normalized_minus1_1"][:, 0]
    arousals = preds["predictions_normalized_minus1_1"][:, 1]

    reset_points()

    for val, ar in zip(valences, arousals):
        mood = map_valence_arousal_to_mood(val, ar)
        add_point_to_visualization(val, ar, mood)

    plot_all_points(audio_file_name + "'s Dynamic Visualization")
