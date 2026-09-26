import requests
import time
import random
import string
import threading

TARGET_URL = 'http://127.0.0.1:5000/api/data'

def fire_request(payload, port):
    try:
        requests.post(TARGET_URL, data=payload, headers={'X-Simulated-Port': str(port)})
    except:
        pass

def normal_traffic():
    print("\n[+] Phase 1: Normal Web Browsing (Safe)")
    for i in range(5):
        fire_request("GET /index.html HTTP/1.1\nUser-Agent: Chrome", 80)
        time.sleep(1)

def attack_exfiltration():
    print("\n[!] Phase 2: DATA EXFILTRATION (Stealing large files)")
    for i in range(2):
        payload = "A" * 5000 # Massive payload
        fire_request(payload, 443)
        time.sleep(1)

def attack_dns_tunnel():
    print("\n[!] Phase 3: DNS TUNNELLING (Encoded Malware Comm.)")
    for i in range(3):
        junk = ''.join(random.choices(string.ascii_letters + string.punctuation, k=50))
        fire_request(junk, 53)
        time.sleep(1)

def attack_port_scan():
    print("\n[!] Phase 4: RECONNAISSANCE / PORT SCANNING (Rapid IP mapping)")
    for port in range(1, 15):
        fire_request("SCAN", port)
        time.sleep(0.1) # Super fast

def attack_ddos():
    print("\n[!] Phase 5: VOLUMETRIC DDoS FLOODING (Crashing the server)")
    for i in range(25):
        fire_request("FLOOD", 80)
        # extremely fast, no sleep

if __name__ == "__main__":
    print("=========================================")
    print(" UNIGUARD AI - MULTI-VECTOR ATTACK TOOL  ")
    print("=========================================")
    
    normal_traffic()
    time.sleep(2)
    
    attack_exfiltration()
    time.sleep(3)
    
    attack_dns_tunnel()
    time.sleep(3)
    
    attack_port_scan()
    time.sleep(3)
    
    attack_ddos()
    
    print("\n[HACKER TERMINAL] All 4 Attack vectors deployed.")
    print(">> View the AI Dashboard to see exactly how the AI caught each unique method!")
