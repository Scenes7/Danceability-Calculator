import librosa

def get_bpm(file_path):
    y, sr = librosa.load(file_path)

    # Estimate tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    return tempo
