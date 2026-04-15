"""
Module 2: Feature Extraction Module
NullRoute - Intelligent Network Traffic Classification and QoS System
"""

import csv
import os

def extract_features(input_path="data/captured_traffic.csv", output_path="data/extracted_features.csv"):
    """
    Reads raw captured packet data and extracts/computes flow-level features.
    Adds derived features used by the classification module.
    """
    print(f"[*] Extracting features from '{input_path}'...")
    rows = []
    with open(input_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pkt_size = float(row["packet_size"])
            duration = float(row["flow_duration"])
            rate = float(row["traffic_rate"])
            dst_port = int(row["dst_port"])
            protocol = row["protocol"]

            # --- Derived Features ---
            bytes_per_second = round(pkt_size * rate / 1000, 2)   # KB/s
            is_high_port = 1 if dst_port > 1024 else 0
            size_category = (
                "small" if pkt_size < 300 else
                "medium" if pkt_size < 900 else
                "large"
            )
            rate_category = (
                "low" if rate < 100 else
                "medium" if rate < 1000 else
                "high"
            )
            duration_category = (
                "short" if duration < 2 else
                "medium" if duration < 30 else
                "long"
            )

            enriched = dict(row)
            enriched["bytes_per_second"] = bytes_per_second
            enriched["is_high_port"] = is_high_port
            enriched["size_category"] = size_category
            enriched["rate_category"] = rate_category
            enriched["duration_category"] = duration_category
            rows.append(enriched)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] Feature extraction complete. {len(rows)} records saved to '{output_path}'")
    return output_path
