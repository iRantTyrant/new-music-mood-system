import os
import shutil

def move_wav_to_output(audio_file_name, source_dir_relative, dest_dir):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, source_dir_relative, audio_file_name)
    dest_path = os.path.join(dest_dir, audio_file_name)

    print(f"[DEBUG] Source path: {source_path}")
    print(f"[DEBUG] Destination path: {os.path.abspath(dest_path)}")

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"⚠️ Το αρχείο δεν βρέθηκε: {source_path}")

    os.makedirs(dest_dir, exist_ok=True)
    shutil.move(source_path, dest_path)
    print(f"[DONE] Μεταφέρθηκε το {audio_file_name} στο {dest_path}")
