from flask import Flask, request, render_template
from flask_cors import CORS
import get_tempo as get_tempo
import tempo_stability as tempo_stability
import librosa
import os
from pydub import AudioSegment


app = Flask(__name__)
CORS(app)

def convert_to_wav(mp3_file_path, wav_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)

    audio.export(wav_file_path, format='wav')

@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['file']
    fileResult = check_if_wav(file.filename)
    if file and fileResult:
        song_path = file.filename
        file.save(song_path)

        if (fileResult == 2):
            new_path = song_path.split('.')[0]+".wav"
            convert_to_wav(song_path, new_path)
            os.remove(song_path)
            song_path = new_path

        duration = librosa.get_duration(path=song_path)
        if (duration > 600): return "Song must be under 10 minutes", 413
        bpm = get_tempo.get_bpm(song_path)
        stability = tempo_stability.calculate_tempo_stability(song_path)
        rating = round(max(0.7*(-0.02*(bpm*bpm-160*bpm+6400)+100), 0) + max(min(30*(stability/16), 30), 0))

        os.remove(song_path)
        return f'{bpm}|{min(100, round(100*(stability/16)))}|{rating}', 200

    return 'Invalid file type', 415

def check_if_wav(filename):
    if ('.' not in filename): return 0

    accepted = ['wav', 'mp3']
    suf = filename.rsplit('.', 1)[1].lower()
    if (suf == accepted[0]): return 1
    elif (suf == accepted[1]): return 2

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()