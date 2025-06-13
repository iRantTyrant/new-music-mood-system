from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='web-app', static_url_path='/')

#Root endpoint
@app.route('/')
def root():
    return app.send_static_file('index.html')

#Endpoint to serve a file from a song 
@app.route('/output/<song>/<filename>')
def output_file(song, filename):
    return send_from_directory(f'output/{song}', filename)

#Endpoint to get the list of the songs (all the directories)
@app.route('/list_songs')
def list_songs():
    songs = [
        d for d in os.listdir('output')
        if os.path.isdir(os.path.join('output', d))
    ]
    return jsonify(songs)

#Endpoint to get the song name (from the wav file)
@app.route('/output/<song>/list_files')
def list_files(song):
    folder_path = os.path.join('output', song)
    files = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    return jsonify(files)
    
#Start the app
if __name__ == '__main__':
    app.run(debug=True)

