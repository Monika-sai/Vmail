from flask import Flask, render_template, request, redirect, url_for
from gtts import gTTS
import os

app = Flask(__name__)

def text_to_speech(text, language='en', output_file='static/output.mp3'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the audio file
    tts.save(output_file)

    return output_file

@app.route('/')
def index():
    return render_template('textToVoice.html')

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        text = request.form['text']
        output_file = text_to_speech(text)
        return render_template('textToVoice.html', audio_file=output_file)

if __name__ == '__main__':
    app.run(debug=True)
