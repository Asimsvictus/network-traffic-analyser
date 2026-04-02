from scapy.all import sniff, IP, TCP
from collections import defaultdict
from datetime import datetime
import logging

# Setup logging to file
logging.basicConfig(
    filename='alerts.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Dictionary to track how many ports each IP has hit
port_scan_tracker = defaultdict(set)

# How many ports triggers an alert
PORT_SCAN_THRESHOLD = 5

def detect_port_scan(packet):
    if IP in packet and TCP in packet:
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport
        flags = packet[TCP].flags

        # SYN flag means a connection attempt
        if flags == 'S':
            port_scan_tracker[src_ip].add(dst_port)
            ports_hit = len(port_scan_tracker[src_ip])

            if ports_hit == PORT_SCAN_THRESHOLD:
                alert = f"PORT SCAN DETECTED — {src_ip} hit {ports_hit} ports"
                print(f"[ALERT] {datetime.now()} — {alert}")
                logging.info(alert)

            elif ports_hit > PORT_SCAN_THRESHOLD and ports_hit % 50 == 0:
                alert = f"PORT SCAN ONGOING — {src_ip} now hit {ports_hit} ports"
                print(f"[ALERT] {datetime.now()} — {alert}")
                logging.info(alert)

def main():
    print("[*] Network Traffic Analyser started")
    print("[*] Listening for port scans...")
    print("[*] Press Ctrl+C to stop\n")
    sniff(iface="eth0", filter="tcp", prn=detect_port_scan, store=0)

if __name__ == "__main__":
    main()
