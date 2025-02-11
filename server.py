from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='build/web')
CORS(app)  # Enable CORS

@app.route('/')
def serve_index():
    return send_from_directory('build/web', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('build/web', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
