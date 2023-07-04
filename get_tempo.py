import librosa

def get_bpm(file_path):
    # Load audio file
    y, sr = librosa.load(file_path)

    # Estimate tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    return tempo

# Provide the path to your audio file (e.g., .wav file)
# audio_file_path = "Fallen Down.wav"

# Get the BPM
# bpm = get_bpm(audio_file_path)
# print("BPM:", bpm)