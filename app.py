from flask import Flask, request, jsonify, send_file
import json
import os
from datetime import datetime

app = Flask(__name__)

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'YOUR_SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'YOUR_SUPABASE_KEY')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        response_id = datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + os.urandom(4).hex()
        
        try:
            from supabase import create_client, Client
            
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            supabase.table('responses').insert({
                'id': response_id,
                'data': data
            }).execute()
            print(f"✅ 数据已保存到 Supabase: {response_id}")
        except Exception as e:
            print(f"⚠️ Supabase 不可用，使用本地存储: {e}")
            DATA_DIR = '/tmp/responses'
            os.makedirs(DATA_DIR, exist_ok=True)
            filename = f"{DATA_DIR}/response_{response_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/responses', methods=['GET'])
def get_responses():
    try:
        from supabase import create_client, Client
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table('responses').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def serve_index():
    return send_file('index.html')

application = app

if __name__ == '__main__':
    print("🚀 问卷服务已启动")
    print("📡 本地访问地址: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)