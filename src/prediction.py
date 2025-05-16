import numpy as np
from essentia.standard import MonoLoader, TensorflowPredictVGGish, TensorflowPredict2D
from src.normalization import normalize_fixed_range_per_column  # Χρήση σωστής συνάρτησης

# Συνάρτηση για πρόβλεψη συναισθήματος
def get_emotion_predictions(audio_path, vggish_model_path, deam_model_path):
    # Φόρτωση ήχου
    audio = MonoLoader(filename=audio_path, sampleRate=16000, resampleQuality=4)()

    # Μοντέλα: embeddings + regression
    embedding_model = TensorflowPredictVGGish(
        graphFilename=vggish_model_path,
        output="model/vggish/embeddings"
    )
    model = TensorflowPredict2D(
        graphFilename=deam_model_path,
        output="model/Identity"
    )

    # Feature extraction και προβλέψεις
    embeddings = embedding_model(audio)
    predictions = np.array(model(embeddings))  # Σχήμα: (Ν, 2) [valence, arousal]

    # Κανονικοποίηση βάσει του DEAM range [1–9]
    predictions_norm_0_1 = normalize_fixed_range_per_column(
        predictions, original_min=1, original_max=9, new_min=0, new_max=1
    )
    predictions_norm_m1_1 = normalize_fixed_range_per_column(
        predictions, original_min=1, original_max=9, new_min=-1, new_max=1
    )

    # Υπολογισμός μέσων όρων
    mean_preds = np.mean(predictions, axis=0)
    mean_preds_norm_0_1 = np.mean(predictions_norm_0_1, axis=0)
    mean_preds_norm_m1_1 = np.mean(predictions_norm_m1_1, axis=0)

    return {
        "predictions": predictions,
        "mean": mean_preds,
        "predictions_normalized_0_1": predictions_norm_0_1,
        "mean_normalized_0_1": mean_preds_norm_0_1,
        "predictions_normalized_minus1_1": predictions_norm_m1_1,
        "mean_normalized_minus1_1": mean_preds_norm_m1_1
    }

