from flask import Flask, render_template, jsonify
import pandas as pd
import pickle
import os
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)
LOG_FILE = 'one_way_telemetry.csv'
MODEL_FILE = 'uniguard_model.pkl'

if not os.path.exists(MODEL_FILE):
    print("Error: Model not found. Run 1_train_model.py first.")
    exit(1)

with open(MODEL_FILE, 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/status')
def status():
    if not os.path.exists(LOG_FILE):
        return jsonify({"total_flows": 0, "alerts": [], "history": []})
        
    try:
        df = pd.read_csv(LOG_FILE, encoding='utf-8')
    except pd.errors.EmptyDataError:
        return jsonify({"total_flows": 0, "alerts": [], "history": []})
        
    if len(df) == 0:
        return jsonify({"total_flows": 0, "alerts": [], "history": []})
        
    # Extract ALL 4 features for the AI Engine
    X = df[['payload_bytes', 'entropy', 'conn_rate', 'distinct_ports']]
    probabilities = model.predict_proba(X)
    
    alerts = []
    history = []
    
    for i, prob in enumerate(probabilities):
        threat_confidence = float(prob[1] * 100)
        is_threat = bool(threat_confidence > 75)
        
        b = int(df.iloc[i]['payload_bytes'])
        e = int(df.iloc[i]['entropy'])
        c = int(df.iloc[i]['conn_rate'])
        p = int(df.iloc[i]['distinct_ports'])
        
        timestamp_full = str(df.iloc[i]['timestamp'])
        
        # Populate history for the 4 charts
        if i >= len(df) - 30:
            history.append({
                "time": timestamp_full[11:19],
                "full_time": timestamp_full,
                "bytes": b, "entropy": e, "rate": c, "ports": p,
                "is_threat": is_threat, "confidence": f"{threat_confidence:.1f}%"
            })
            
        if is_threat:
            # Diagnose the exact attack type based on feature spikes
            analysis = []
            attack_name = "Generic Threat"
            
            if p >= 5:
                attack_name = "Port Scanning / Reconnaissance"
                analysis.append(f"Targeted {p} distinct ports rapidly")
            elif c >= 15:
                attack_name = "DDoS / Volumetric Flood"
                analysis.append(f"Connection rate spiked to {c} req/5s")
            elif e > 20:
                attack_name = "DNS Tunneling / Encoded Payload"
                analysis.append(f"High data entropy detected ({e} spec chars)")
            elif b > 2000:
                attack_name = "Data Exfiltration"
                analysis.append(f"Abnormal data volume ({b} bytes)")
                
            alerts.append({
                "time": timestamp_full[:19].replace('T', ' '),
                "ip": str(df.iloc[i]['source_ip']),
                "confidence": f"{threat_confidence:.1f}%",
                "attack_type": attack_name,
                "details": " | ".join(analysis),
                "preview": str(df.iloc[i].get('raw_preview', 'N/A'))
            })
            
    return jsonify({
        "total_flows": len(df),
        "alerts": alerts[::-1][:15], 
        "history": history
    })

if __name__ == '__main__':
    app.run(port=5001, threaded=True)
