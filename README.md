# Project Overview

This project processes `.wav` audio files using a pipeline defined in `main.py`. The pipeline handles loading the audio files, processing them, and extracting all necessary information.

## Setup Instructions

# Very important to download the .pb files (the models/weight) from Essentia for the VGGISH-Deam Valence-Arousal predictor , and the VGGISH-3 audioset extractor (info can be found in their respective .json files in the models directory / folder)

1. **Add Audio Files**  
   Place your `.wav` audio files in the `data` folder. These files will be automatically loaded and processed by the pipeline in `main.py`.

2. **Create a Python Virtual Environment**  
   Ensure you are using Python 3.7 for this project. To create a virtual environment, run the following commands in your terminal:
   ```bash
   python3.7 -m venv venv # Or whatever name you want here 
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt