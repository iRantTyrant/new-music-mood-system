from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='web-app', static_url_path='/')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/output/<song>/<filename>')
def output_file(song, filename):
    return send_from_directory(f'output/{song}', filename)

@app.route('/list_songs')
def list_songs():
    songs = [
        d for d in os.listdir('output')
        if os.path.isdir(os.path.join('output', d))
    ]
    return jsonify(songs)

if __name__ == '__main__':
    app.run(debug=True)
