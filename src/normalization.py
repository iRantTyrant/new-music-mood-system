#Import necessary library
import numpy as np

#The actual function 
def normalize_fixed_range_per_column(values, original_min, original_max, new_min, new_max):
    values = np.array(values, dtype=float)
    norm_values = np.zeros_like(values)

    # For every column (valence/arousal) get its normalized value
    for i in range(values.shape[1]):  
        col = values[:, i]
        norm_values[:, i] = (col - original_min) / (original_max - original_min) * (new_max - new_min) + new_min

    return norm_values

