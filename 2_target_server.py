from flask import Flask, request
import datetime
import os
import csv
import logging
import time

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)
LOG_FILE = 'one_way_telemetry.csv'

# Behavioral State Tracker (Tracks IPs to detect Scans and DDoS)
ip_state = {}

# For the prototype, always start with a clean slate when server boots
if os.path.exists(LOG_FILE):
    try:
        os.remove(LOG_FILE)
    except Exception:
        pass

# Initialize log file with the new 7-column headers
with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'source_ip', 'payload_bytes', 'entropy', 'conn_rate', 'distinct_ports', 'raw_preview'])

@app.route('/api/data', methods=['POST'])
def receive_data():
    ip = request.remote_addr
    data = request.get_data(as_text=True)
    port = int(request.headers.get('X-Simulated-Port', 80)) # Hackers hit different ports
    
    now = time.time()
    
    # 1. Update Behavioral State for this IP (Clean history older than 5 seconds)
    if ip not in ip_state:
        ip_state[ip] = []
    ip_state[ip] = [req for req in ip_state[ip] if now - req[0] < 5.0]
    
    # Add current request
    ip_state[ip].append((now, port))
    
    # 2. Extract Deep Network Features
    payload_bytes = len(data)
    entropy = sum(not c.isalnum() and not c.isspace() for c in data)
    conn_rate = len(ip_state[ip]) # How many connections in last 5s?
    distinct_ports = len(set(p for t, p in ip_state[ip])) # How many unique ports in last 5s?
    
    raw_preview = data[:30] + '...' if len(data) > 30 else data.replace('\n', ' ')
    
    print(f"[+] INBOUND TRAFFIC | Size: {payload_bytes}B | Entropy: {entropy} | Rate: {conn_rate}/5s | Ports: {distinct_ports}")
    
    # 3. Transmit via Data Diode (One-Way)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().isoformat(), 
            ip, 
            payload_bytes, 
            entropy,
            conn_rate,
            distinct_ports,
            raw_preview
        ])
    
    return "Data received securely\n", 200

if __name__ == '__main__':
    print("=== PROTECTED TARGET SERVER RUNNING (Port 5000) ===")
    print(" Tracking Behavioral Telemetry (State, Rates, Ports) over time...")
    app.run(port=5000, threaded=True)
