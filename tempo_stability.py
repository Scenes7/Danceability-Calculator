import aubio

def calculate_tempo_stability(file_path):
    # Create aubio tempo object
    tempo = aubio.tempo()

    # Open the audio file
    audio_file = aubio.source(file_path)

    # Initialize variables
    previous_tempo = 0.0
    tempo_stability = 0.0
    num_tempo_changes = 0

    # Process audio frames
    while True:
        samples, read = audio_file()
        is_beat = tempo(samples)

        # Check if a new tempo is detected
        if is_beat:
            current_tempo = tempo.get_bpm()

            # Calculate tempo stability
            if previous_tempo != 0.0 and abs(current_tempo - previous_tempo) > 1.0:
                tempo_stability += abs(current_tempo - previous_tempo)
                num_tempo_changes += 1

            previous_tempo = current_tempo

        if read < audio_file.hop_size:
            break

    # Close the audio file
    audio_file.close()

    if num_tempo_changes > 0:
        avg_tempo_stability = tempo_stability / num_tempo_changes
        return avg_tempo_stability
    else:
        return 0.0

# Example usage
# file_path = "Galaxy Collapse.wav" #13
# file_path = "Fallen Down.wav" #14
# file_path = "11 Thinking Out Loud.wav" #15

# file_path = "moonlightMov1.wav" #
# tempo_stability = calculate_tempo_stability(file_path)
# print(f"Tempo stability: {tempo_stability}")