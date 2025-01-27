from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/verse_requestor', methods=['POST'])
def get_verse():
    data = request.get_json()

    verse_reference = data.get('reference')

    if not verse_reference:
        
        return jsonify({"error": "No reference given"}), 400

    command = f"./Release/verse_requestor {verse_reference}"
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stdout, "query": data}), 500

@app.route('/verse_search', methods=['POST'])
def search_verses():
    data = request.json
    search_term = data.get('search_term')

    if not search_term:
        return jsonify({"error": "No search term given"}), 400

    command = f"./Release/verse_search {search_term}"
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)