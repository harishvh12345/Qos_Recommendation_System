"""
Module 4: QoS Recommendation Module
NullRoute - Intelligent Network Traffic Classification and QoS System

Implements QoS principles based on:
  - RFC 4594: Configuration Guidelines for DiffServ Service Classes
  - IEEE 802.1p: Layer 2 Priority Tagging
  - ITU-T G.1010: Quality of Service for Multimedia Applications
"""

import csv
import os

# ── QoS Policy Table ────────────────────────────────────────────────────────────
#
#  DSCP (Differentiated Services Code Point) values per RFC 4594
#  IEEE 802.1p priority (0=lowest, 7=highest)
#  Scheduling: WFQ (Weighted Fair Queuing), PQ (Priority Queue), BE (Best Effort)
#
QOS_POLICY = {
    "voip": {
        "priority_level": 1,          # Highest
        "priority_name": "CRITICAL",
        "dscp_value": 46,             # EF - Expedited Forwarding
        "dscp_name": "EF (Expedited Forwarding)",
        "ieee_priority": 6,
        "scheduling": "Priority Queue (PQ)",
        "bandwidth_guarantee": "10%",
        "max_delay_ms": 150,
        "max_jitter_ms": 30,
        "packet_loss_tolerance": "< 1%",
        "queue_depth": "Small (low latency)",
        "rationale": "Real-time voice requires ultra-low latency and jitter. Per ITU-T G.114, max one-way delay must be <150ms for acceptable voice quality.",
        "color": "#FF4757"
    },
    "multimedia": {
        "priority_level": 2,
        "priority_name": "HIGH",
        "dscp_value": 34,             # AF41 - Assured Forwarding
        "dscp_name": "AF41 (Assured Forwarding 4-1)",
        "ieee_priority": 5,
        "scheduling": "Weighted Fair Queuing (WFQ)",
        "bandwidth_guarantee": "30%",
        "max_delay_ms": 400,
        "max_jitter_ms": 100,
        "packet_loss_tolerance": "< 2%",
        "queue_depth": "Medium",
        "rationale": "Video streaming requires consistent bandwidth and bounded delay. WFQ ensures fair sharing during congestion while maintaining playback quality.",
        "color": "#FFA502"
    },
    "gaming": {
        "priority_level": 3,
        "priority_name": "HIGH",
        "dscp_value": 40,             # CS5
        "dscp_name": "CS5 (Class Selector 5)",
        "ieee_priority": 5,
        "scheduling": "Weighted Fair Queuing (WFQ)",
        "bandwidth_guarantee": "15%",
        "max_delay_ms": 100,
        "max_jitter_ms": 20,
        "packet_loss_tolerance": "< 1%",
        "queue_depth": "Small",
        "rationale": "Interactive gaming is latency-sensitive. Low delay and jitter are critical for real-time game state synchronization.",
        "color": "#ECCC68"
    },
    "web": {
        "priority_level": 4,
        "priority_name": "MEDIUM",
        "dscp_value": 26,             # AF31
        "dscp_name": "AF31 (Assured Forwarding 3-1)",
        "ieee_priority": 3,
        "scheduling": "Weighted Fair Queuing (WFQ)",
        "bandwidth_guarantee": "25%",
        "max_delay_ms": 1000,
        "max_jitter_ms": 500,
        "packet_loss_tolerance": "< 3%",
        "queue_depth": "Medium",
        "rationale": "Web browsing is interactive but tolerates moderate latency. TCP's retransmission handles packet loss, so some queuing delay is acceptable.",
        "color": "#2ED573"
    },
    "file_transfer": {
        "priority_level": 5,
        "priority_name": "LOW",
        "dscp_value": 10,             # AF11
        "dscp_name": "AF11 (Assured Forwarding 1-1)",
        "ieee_priority": 2,
        "scheduling": "Deficit Round Robin (DRR)",
        "bandwidth_guarantee": "15%",
        "max_delay_ms": 5000,
        "max_jitter_ms": 2000,
        "packet_loss_tolerance": "< 5%",
        "queue_depth": "Large",
        "rationale": "Bulk file transfers benefit from large queues and can tolerate delay. TCP ensures reliable delivery. DRR provides fair bulk throughput.",
        "color": "#1E90FF"
    },
    "background": {
        "priority_level": 6,          # Lowest
        "priority_name": "BEST EFFORT",
        "dscp_value": 0,              # BE - Best Effort
        "dscp_name": "BE (Best Effort / Default)",
        "ieee_priority": 0,
        "scheduling": "Best Effort (FIFO)",
        "bandwidth_guarantee": "5%",
        "max_delay_ms": 10000,
        "max_jitter_ms": 5000,
        "packet_loss_tolerance": "< 10%",
        "queue_depth": "Default",
        "rationale": "Control/management traffic (DNS, NTP, SNMP) consumes minimal bandwidth. Best effort delivery is acceptable for infrequent control messages.",
        "color": "#747D8C"
    }
}

def apply_qos(input_path="data/classified_traffic.csv", output_path="data/qos_recommended.csv"):
    """
    Reads classified traffic and applies QoS policy recommendations.
    Adds DSCP marking, priority, scheduling class, and SLA parameters.
    """
    print(f"[*] Applying QoS recommendations from '{input_path}'...")
    rows = []
    with open(input_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row["classified_label"]
            policy = QOS_POLICY.get(label, QOS_POLICY["background"])

            row["qos_priority"] = policy["priority_level"]
            row["qos_priority_name"] = policy["priority_name"]
            row["dscp_value"] = policy["dscp_value"]
            row["dscp_name"] = policy["dscp_name"]
            row["ieee_8021p"] = policy["ieee_priority"]
            row["scheduling_class"] = policy["scheduling"]
            row["bandwidth_guarantee"] = policy["bandwidth_guarantee"]
            row["max_delay_ms"] = policy["max_delay_ms"]
            row["max_jitter_ms"] = policy["max_jitter_ms"]
            row["packet_loss_tolerance"] = policy["packet_loss_tolerance"]
            rows.append(row)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] QoS recommendations applied to {len(rows)} packets.")
    print(f"    Output saved to '{output_path}'")

    # Summary
    from collections import Counter
    priority_counts = Counter(r["qos_priority_name"] for r in rows)
    print("\n    QoS Priority Distribution:")
    for p, count in sorted(priority_counts.items()):
        print(f"      {p}: {count} packets")

    return output_path, QOS_POLICY
