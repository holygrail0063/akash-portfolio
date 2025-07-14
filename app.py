from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import socket

app = Flask(__name__, static_folder='static')

# Initialize visit counter
COUNTER_FILE = 'visit_counter.json'

def load_visit_count():
    try:
        with open(COUNTER_FILE, 'r') as f:
            data = json.load(f)
            return data.get('visits', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_visit_count(count):
    with open(COUNTER_FILE, 'w') as f:
        json.dump({'visits': count}, f)

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
    # Increment visit count
    visit_count = load_visit_count() + 1
    save_visit_count(visit_count)
    
    # Format visit count for display
    formatted_count = f"{visit_count:,}"
    if visit_count >= 1000:
        formatted_count = f"{visit_count/1000:.1f}k"
    
    return render_template('index.html', visit_count=formatted_count)

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
