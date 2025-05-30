#Import necessary libraries and functions
import numpy as np
from essentia.standard import MonoLoader, TensorflowPredictVGGish, TensorflowPredict2D
from src.normalization import normalize_fixed_range_per_column  # Χρήση σωστής συνάρτησης

# The actual function
def get_emotion_predictions(audio_path, vggish_model_path, deam_model_path):
    
    # Load the audio
    audio = MonoLoader(filename=audio_path, sampleRate=16000, resampleQuality=4)()

    # Take the models for the extraction and prediction
    embedding_model = TensorflowPredictVGGish(
        graphFilename=vggish_model_path,
        output="model/vggish/embeddings"
    )
    model = TensorflowPredict2D(
        graphFilename=deam_model_path,
        output="model/Identity"
    )

    # Get the values for the exctraction(embeddings) and then predict their valence arousal
    embeddings = embedding_model(audio)
    predictions = np.array(model(embeddings))  # (Ν, 2) [valence, arousal]

    #Normalization for the DEAM range from [1–9] -> [0-1] && [(-1)-1]
    predictions_norm_0_1 = normalize_fixed_range_per_column(
        predictions, original_min=1, original_max=9, new_min=0, new_max=1
    )
    predictions_norm_m1_1 = normalize_fixed_range_per_column(
        predictions, original_min=1, original_max=9, new_min=-1, new_max=1
    )

    # Get mean values for all predictions
    mean_preds = np.mean(predictions, axis=0)
    mean_preds_norm_0_1 = np.mean(predictions_norm_0_1, axis=0)
    mean_preds_norm_m1_1 = np.mean(predictions_norm_m1_1, axis=0)

    #We return everything so we can use whatever we want
    return {
        "predictions": predictions,
        "mean": mean_preds,
        "predictions_normalized_0_1": predictions_norm_0_1,
        "mean_normalized_0_1": mean_preds_norm_0_1,
        "predictions_normalized_minus1_1": predictions_norm_m1_1,
        "mean_normalized_minus1_1": mean_preds_norm_m1_1
    }

