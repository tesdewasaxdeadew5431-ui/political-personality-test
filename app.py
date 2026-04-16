from flask import Flask, request, jsonify, send_file
import json
import os
from datetime import datetime

app = Flask(__name__)

def get_supabase_client():
    try:
        from supabase import create_client, Client
        url = os.environ.get('SUPABASE_URL', 'https://gunxvxbapgnuzqoghsax.supabase.co')
        key = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1bnh2eGJhcGdudXpxb2doc2F4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYzMDMyMTUsImV4cCI6MjA5MTg3OTIxNX0.33BCBTh-uNg0JBDA9Pps_FfKRNtWGoeiXt-7qKKcgx4')
        return create_client(url, key)
    except Exception as e:
        print(f"Failed to create Supabase client: {e}")
        return None

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        response_id = datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + os.urandom(4).hex()
        
        supabase = get_supabase_client()
        if supabase:
            try:
                supabase.table('responses').insert({
                    'id': response_id,
                    'data': data
                }).execute()
                print(f"✅ Saved to Supabase: {response_id}")
            except Exception as e:
                print(f"❌ Supabase error: {e}")
                raise
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/responses', methods=['GET'])
def get_responses():
    try:
        supabase = get_supabase_client()
        if supabase:
            response = supabase.table('responses').select('*').execute()
            return jsonify(response.data)
        return jsonify([])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def serve_index():
    return send_file('index.html')

application = app

if __name__ == '__main__':
    print("🚀 Server started")
    print("📡 Local: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)