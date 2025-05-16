import numpy as np

def normalize_fixed_range_per_column(values, original_min=1, original_max=9, new_min=0, new_max=1):
    values = np.array(values, dtype=float)
    norm_values = np.zeros_like(values)

    for i in range(values.shape[1]):  # Για κάθε στήλη (valence/arousal)
        col = values[:, i]
        norm_values[:, i] = (col - original_min) / (original_max - original_min) * (new_max - new_min) + new_min

    return norm_values

