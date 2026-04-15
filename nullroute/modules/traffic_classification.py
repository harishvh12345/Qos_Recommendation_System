"""
Module 3: Traffic Classification Module
NullRoute - Intelligent Network Traffic Classification and QoS System

Rule-Based Intelligent Classification Engine
Based on: RFC 4594 (QoS), IEEE 802.1p, standard port assignments (IANA)
"""

import csv
import os

# ── Classification Rules (Priority Order) ──────────────────────────────────────
#
#  Each rule is a dict with match conditions + result label.
#  Rules are evaluated top-to-bottom; first match wins.
#  This mirrors how real network devices (routers/firewalls) classify traffic.
#
CLASSIFICATION_RULES = [
    # VoIP - Real-time, small UDP, low rate, known SIP/RTP ports
    {
        "name": "VoIP (SIP/RTP)",
        "protocol": "UDP",
        "port_range": (5060, 5061),
        "label": "voip"
    },
    {
        "name": "VoIP RTP Media",
        "protocol": "UDP",
        "port_range": (16384, 16385),
        "label": "voip"
    },
    # Gaming - UDP, moderate rate, known game ports
    {
        "name": "Online Gaming",
        "protocol": "UDP",
        "port_range": (3074, 3074),
        "label": "gaming"
    },
    {
        "name": "Online Gaming (Steam/Other)",
        "protocol": "UDP",
        "port_range": (27000, 27030),
        "label": "gaming"
    },
    # Multimedia streaming - UDP, large packets, high rate
    {
        "name": "Video Streaming (RTSP)",
        "protocol": "UDP",
        "port_range": (554, 554),
        "label": "multimedia"
    },
    {
        "name": "Video Streaming (RTMP)",
        "protocol": "TCP",
        "port_range": (1935, 1935),
        "label": "multimedia"
    },
    {
        "name": "RTP Streams",
        "protocol": "UDP",
        "port_range": (5004, 5005),
        "label": "multimedia"
    },
    # File Transfer - TCP, large packets, high sustained rate
    {
        "name": "FTP Data/Control",
        "protocol": "TCP",
        "port_range": (20, 21),
        "label": "file_transfer"
    },
    {
        "name": "SSH/SCP",
        "protocol": "TCP",
        "port_range": (22, 22),
        "label": "file_transfer"
    },
    {
        "name": "SMB File Share",
        "protocol": "TCP",
        "port_range": (445, 445),
        "label": "file_transfer"
    },
    {
        "name": "NFS",
        "protocol": "TCP",
        "port_range": (2049, 2049),
        "label": "file_transfer"
    },
    # Background - DNS, NTP, SNMP, DHCP, ICMP
    {
        "name": "DNS",
        "protocol": "UDP",
        "port_range": (53, 53),
        "label": "background"
    },
    {
        "name": "NTP",
        "protocol": "UDP",
        "port_range": (123, 123),
        "label": "background"
    },
    {
        "name": "SNMP",
        "protocol": "UDP",
        "port_range": (161, 162),
        "label": "background"
    },
    {
        "name": "DHCP",
        "protocol": "UDP",
        "port_range": (67, 68),
        "label": "background"
    },
    {
        "name": "ICMP",
        "protocol": "ICMP",
        "port_range": (0, 65535),
        "label": "background"
    },
    # Web - TCP, HTTP/HTTPS ports
    {
        "name": "HTTP Web",
        "protocol": "TCP",
        "port_range": (80, 80),
        "label": "web"
    },
    {
        "name": "HTTPS Web",
        "protocol": "TCP",
        "port_range": (443, 443),
        "label": "web"
    },
    {
        "name": "HTTP Alt",
        "protocol": "TCP",
        "port_range": (8080, 8080),
        "label": "web"
    },
]

def classify_packet(protocol, dst_port, packet_size, traffic_rate, flow_duration):
    """
    Applies classification rules to a single packet's features.
    Returns (label, matched_rule_name, confidence)
    """
    dst_port = int(dst_port)
    packet_size = float(packet_size)
    traffic_rate = float(traffic_rate)
    flow_duration = float(flow_duration)

    # Step 1: Port + Protocol based rules
    for rule in CLASSIFICATION_RULES:
        port_lo, port_hi = rule["port_range"]
        if rule["protocol"] == protocol and port_lo <= dst_port <= port_hi:
            return rule["label"], rule["name"], "HIGH"

    # Step 2: Heuristic fallback rules (when no port match)
    # Inspired by DSCP / DiffServ classification principles
    if protocol == "UDP":
        if packet_size < 250 and traffic_rate < 200 and flow_duration > 5:
            return "voip", "Heuristic: Small UDP long-lived", "MEDIUM"
        if packet_size > 700 and traffic_rate > 400:
            return "multimedia", "Heuristic: Large-packet high-rate UDP", "MEDIUM"
        if traffic_rate < 60:
            return "background", "Heuristic: Low-rate UDP", "MEDIUM"

    if protocol == "TCP":
        if packet_size > 900 and traffic_rate > 900 and flow_duration > 5:
            return "file_transfer", "Heuristic: Bulk TCP transfer", "MEDIUM"
        if packet_size > 500 and traffic_rate > 400:
            return "multimedia", "Heuristic: High-rate large TCP", "LOW"
        if 200 <= packet_size <= 1400 and flow_duration < 10:
            return "web", "Heuristic: Moderate TCP short flow", "LOW"

    return "background", "Default: Unclassified", "LOW"


def classify_traffic(input_path="data/extracted_features.csv", output_path="data/classified_traffic.csv"):
    """
    Classifies each packet in the extracted features dataset.
    """
    print(f"[*] Classifying traffic from '{input_path}'...")
    rows = []
    correct = 0
    total = 0

    with open(input_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label, rule_name, confidence = classify_packet(
                row["protocol"],
                row["dst_port"],
                row["packet_size"],
                row["traffic_rate"],
                row["flow_duration"]
            )
            row["classified_label"] = label
            row["matched_rule"] = rule_name
            row["confidence"] = confidence
            row["is_correct"] = "YES" if label == row["true_label"] else "NO"
            if label == row["true_label"]:
                correct += 1
            total += 1
            rows.append(row)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    accuracy = round((correct / total) * 100, 2) if total else 0
    print(f"[+] Classification complete. Accuracy: {accuracy}% ({correct}/{total})")
    print(f"    Results saved to '{output_path}'")
    return output_path, accuracy
