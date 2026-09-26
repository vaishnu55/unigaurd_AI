import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

print("--- Generating Synthetic Advanced Network Telemetry ---")
np.random.seed(42)

# 1. Normal Web Traffic
n_norm = 1500
df_normal = pd.DataFrame({
    'payload_bytes': np.random.normal(300, 100, n_norm).astype(int),
    'entropy': np.random.poisson(2, n_norm),
    'conn_rate': np.random.poisson(2, n_norm), # Connections per 5 seconds
    'distinct_ports': np.random.poisson(1, n_norm), # Ports accessed
    'is_threat': 0
})

# 2. ATTACK: Data Exfiltration (Massive payload volume)
n_exfil = 200
df_exfil = pd.DataFrame({
    'payload_bytes': np.random.normal(5000, 1000, n_exfil).astype(int),
    'entropy': np.random.poisson(5, n_exfil),
    'conn_rate': np.random.poisson(2, n_exfil),
    'distinct_ports': np.random.poisson(1, n_exfil),
    'is_threat': 1
})

# 3. ATTACK: DNS Tunneling / Encoded Payload (High Entropy)
n_dns = 200
df_dns = pd.DataFrame({
    'payload_bytes': np.random.normal(150, 50, n_dns).astype(int),
    'entropy': np.random.poisson(55, n_dns),
    'conn_rate': np.random.poisson(2, n_dns),
    'distinct_ports': np.random.poisson(1, n_dns),
    'is_threat': 1
})

# 4. ATTACK: Port Scanning / Reconnaissance (High Distinct Ports)
n_scan = 200
df_scan = pd.DataFrame({
    'payload_bytes': np.random.normal(50, 20, n_scan).astype(int),
    'entropy': np.random.poisson(1, n_scan),
    'conn_rate': np.random.poisson(15, n_scan),
    'distinct_ports': np.random.normal(15, 3, n_scan).astype(int),
    'is_threat': 1
})

# 5. ATTACK: DDoS / Volumetric Flooding (Extremely High Connection Rate)
n_ddos = 200
df_ddos = pd.DataFrame({
    'payload_bytes': np.random.normal(100, 20, n_ddos).astype(int),
    'entropy': np.random.poisson(1, n_ddos),
    'conn_rate': np.random.normal(40, 10, n_ddos).astype(int),
    'distinct_ports': np.random.poisson(1, n_ddos),
    'is_threat': 1
})

# Combine, clean, and shuffle
df = pd.concat([df_normal, df_exfil, df_dns, df_scan, df_ddos]).sample(frac=1).reset_index(drop=True)
df[df < 0] = 0 # Remove negative anomalies

# Extract Features
X = df[['payload_bytes', 'entropy', 'conn_rate', 'distinct_ports']]
y = df['is_threat']

print("--- Training Advanced AI Model (Random Forest) ---")
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X, y)

# Save the trained model
with open('uniguard_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("--- Advanced Multi-Vector AI Model Saved! ---")
