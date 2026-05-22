from flask import Flask, render_template, request, jsonify, send_file, Response
import json
import os
import socket
from datetime import datetime, timezone

app = Flask(__name__, static_folder='static')
SITE_URL = os.environ.get('SITE_URL', 'https://www.akashkamble.ca').rstrip('/')

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
    return send_file(os.path.join(app.static_folder, 'resume.pdf'), mimetype='application/pdf')

@app.route('/resume.pdf')
def serve_resume_lowercase():
    return serve_resume()

@app.route('/robots.txt')
def robots_txt():
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    return Response(content, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap_xml():
    lastmod = datetime.now(timezone.utc).date().isoformat()
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{SITE_URL}/Resume.pdf</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>
"""
    return Response(content, mimetype='application/xml')


if __name__ == '__main__':
    app.run(debug=True, port=5000) 
