import numpy as np
from essentia.standard import MonoLoader, TensorflowPredictVGGish, TensorflowPredict2D

def normalize_minmax(values, new_min=0, new_max=1):
    old_min = np.min(values)
    old_max = np.max(values)
    if old_max - old_min == 0:
        return np.zeros_like(values) + new_min  # αποφυγή διαίρεσης με μηδέν
    return (values - old_min) / (old_max - old_min) * (new_max - new_min) + new_min

def get_emotion_predictions(audio_path, vggish_model_path, deam_model_path):
    audio = MonoLoader(filename=audio_path, sampleRate=16000, resampleQuality=4)()
    embedding_model = TensorflowPredictVGGish(graphFilename=vggish_model_path, output="model/vggish/embeddings")
    model = TensorflowPredict2D(graphFilename=deam_model_path, output="model/Identity")

    embeddings = embedding_model(audio)
    predictions = model(embeddings)
    predictions = np.array(predictions)

    mean_preds = np.mean(predictions, axis=0)

    # Κανονικοποίηση με βάση τα πραγματικά min-max των δεδομένων
    predictions_norm_0_1 = normalize_minmax(predictions, 0, 1)
    mean_preds_norm_0_1 = normalize_minmax(mean_preds, 0, 1)

    predictions_norm_minus1_1 = normalize_minmax(predictions, -1, 1)
    mean_preds_norm_minus1_1 = normalize_minmax(mean_preds, -1, 1)

    return {
        "predictions": predictions,
        "mean": mean_preds,
        "predictions_normalized_0_1": predictions_norm_0_1,
        "mean_normalized_0_1": mean_preds_norm_0_1,
        "predictions_normalized_minus1_1": predictions_norm_minus1_1,
        "S": mean_preds_norm_minus1_1
    }
    
