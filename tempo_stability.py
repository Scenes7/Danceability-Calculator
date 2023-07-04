import aubio

def calculate_tempo_stability(file_path):
    tempo = aubio.tempo()

    audio_file = aubio.source(file_path)

    previous_tempo = 0.0
    tempo_stability = 0.0
    num_tempo_changes = 0

    while True:
        samples, read = audio_file()
        is_beat = tempo(samples)

        if is_beat:
            current_tempo = tempo.get_bpm()

            # Calculate tempo stability
            if previous_tempo != 0.0 and abs(current_tempo - previous_tempo) > 1.0:
                tempo_stability += abs(current_tempo - previous_tempo)
                num_tempo_changes += 1

            previous_tempo = current_tempo

        if read < audio_file.hop_size:
            break

    audio_file.close()

    if num_tempo_changes > 0:
        avg_tempo_stability = tempo_stability / num_tempo_changes
        return avg_tempo_stability
    return 0.0