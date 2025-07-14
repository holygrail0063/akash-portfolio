from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import socket

app = Flask(__name__, static_folder='static')

# Counter file path
COUNTER_FILE = 'visit_counter.json'

def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            return json.load(f)
    return {'visits': 0}

def save_counter(counter_data):
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counter_data, f)

def get_local_ip():
    try:
        # Get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

@app.route('/')
def home():
    counter_data = load_counter()
    counter_data['visits'] += 1
    save_counter(counter_data)
    return render_template('index.html', visit_count=counter_data['visits'])

@app.route('/api/visit-count')
def get_visit_count():
    counter_data = load_counter()
    return jsonify({'visits': counter_data['visits']})

@app.route('/Resume.pdf')
def serve_resume():
    return send_file('Resume.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    local_ip = get_local_ip()
    print(f"\nLocal server URLs:")
    print(f"Computer access: http://localhost:5000")
    print(f"Mobile access: http://{local_ip}:5000")
    print("\nShare the mobile access URL with devices on your network to test mobile view.")
    app.run(host='0.0.0.0', port=5000, debug=True) 
