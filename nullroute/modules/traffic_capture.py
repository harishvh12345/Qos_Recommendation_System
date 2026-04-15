"""
Module 1: Network Traffic Capture Module
NullRoute - Intelligent Network Traffic Classification and QoS System
Team: Vishal, Vishwa J, Harish V | Reg: 25MAI1003, 25MAI1004, 25MAI1019
"""

import csv
import random
import time
import os
from datetime import datetime

# --- Simulated Traffic Profiles (mimics real Wireshark packet capture) ---
TRAFFIC_PROFILES = {
    "web": {
        "protocols": ["TCP"],
        "ports": [80, 443, 8080],
        "packet_size_range": (200, 1400),
        "flow_duration_range": (0.5, 5.0),
        "rate_range": (50, 500),
    },
    "multimedia": {
        "protocols": ["UDP"],
        "ports": [554, 1935, 5004, 5005],
        "packet_size_range": (800, 1500),
        "flow_duration_range": (10, 120),
        "rate_range": (500, 8000),
    },
    "file_transfer": {
        "protocols": ["TCP"],
        "ports": [21, 22, 445, 2049],
        "packet_size_range": (1000, 1500),
        "flow_duration_range": (5, 60),
        "rate_range": (1000, 10000),
    },
    "background": {
        "protocols": ["UDP", "ICMP", "TCP"],
        "ports": [53, 123, 161, 67, 68],
        "packet_size_range": (40, 300),
        "flow_duration_range": (0.01, 1.0),
        "rate_range": (1, 50),
    },
    "voip": {
        "protocols": ["UDP"],
        "ports": [5060, 5061, 16384, 16385],
        "packet_size_range": (60, 220),
        "flow_duration_range": (5, 300),
        "rate_range": (64, 128),
    },
    "gaming": {
        "protocols": ["UDP"],
        "ports": [3074, 3478, 7777, 27015],
        "packet_size_range": (50, 500),
        "flow_duration_range": (60, 3600),
        "rate_range": (30, 300),
    },
}

PRIVATE_SUBNETS = [
    "192.168.1.", "192.168.0.", "10.0.0.", "172.16.0."
]

def random_ip(private=True):
    subnet = random.choice(PRIVATE_SUBNETS)
    return subnet + str(random.randint(1, 254))

def random_public_ip():
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def generate_flow_id():
    return f"FLOW-{random.randint(10000,99999)}"

def capture_traffic(num_packets=300, output_path="data/captured_traffic.csv"):
    """
    Simulates capturing network packets from a LAN environment.
    In a real environment, this would use Scapy or pyshark to read from an interface.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = [
        "timestamp", "flow_id", "src_ip", "dst_ip",
        "src_port", "dst_port", "protocol",
        "packet_size", "flow_duration", "traffic_rate",
        "true_label"
    ]
    packets = []
    print(f"[*] Starting simulated packet capture ({num_packets} packets)...")
    categories = list(TRAFFIC_PROFILES.keys())
    weights = [0.30, 0.25, 0.15, 0.15, 0.10, 0.05]

    for i in range(num_packets):
        label = random.choices(categories, weights=weights, k=1)[0]
        profile = TRAFFIC_PROFILES[label]
        protocol = random.choice(profile["protocols"])
        port = random.choice(profile["ports"])
        pkt_size = random.randint(*profile["packet_size_range"])
        duration = round(random.uniform(*profile["flow_duration_range"]), 3)
        rate = round(random.uniform(*profile["rate_range"]), 2)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.") + str(random.randint(100, 999))

        packet = {
            "timestamp": timestamp,
            "flow_id": generate_flow_id(),
            "src_ip": random_ip(),
            "dst_ip": random_public_ip() if label != "background" else random_ip(),
            "src_port": random.randint(1024, 65535),
            "dst_port": port,
            "protocol": protocol,
            "packet_size": pkt_size,
            "flow_duration": duration,
            "traffic_rate": rate,
            "true_label": label
        }
        packets.append(packet)
        if (i + 1) % 50 == 0:
            print(f"    Captured {i+1}/{num_packets} packets...")

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(packets)

    print(f"[+] Capture complete. {num_packets} packets saved to '{output_path}'")
    return output_path
