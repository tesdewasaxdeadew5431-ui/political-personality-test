from flask import Flask, request, jsonify, send_file
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'responses'
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        response_id = datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + os.urandom(4).hex()
        filename = f"{DATA_DIR}/response_{response_id}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/responses', methods=['GET'])
def get_responses():
    files = sorted(os.listdir(DATA_DIR))
    responses = []
    for f in files:
        if f.endswith('.json'):
            filepath = os.path.join(DATA_DIR, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                responses.append(data)
    return jsonify(responses)

@app.route('/')
def serve_index():
    return send_file('index.html')

if __name__ == '__main__':
    print("🚀 问卷服务已启动")
    print("📡 本地访问地址: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)