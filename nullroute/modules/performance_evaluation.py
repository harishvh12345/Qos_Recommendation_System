"""
Module 5: Performance Evaluation Module
NullRoute - Intelligent Network Traffic Classification and QoS System

Computes network performance metrics BEFORE and AFTER QoS recommendations.
Simulates what happens when traffic is prioritized according to QoS policy.
"""

import csv
import os
import random
from collections import defaultdict

def simulate_without_qos(rows):
    """
    Simulates network behavior WITHOUT QoS (FIFO / Best Effort for all traffic).
    All flows share bandwidth equally — real-time traffic suffers.
    """
    results = {}
    total_bandwidth = 100.0  # Mbps baseline

    for label in set(r["classified_label"] for r in rows):
        pkts = [r for r in rows if r["classified_label"] == label]
        if not pkts:
            continue
        avg_rate = sum(float(p["traffic_rate"]) for p in pkts) / len(pkts)
        # No prioritization => simulated congestion adds delay to all equally
        congestion_factor = random.uniform(1.5, 3.5)
        results[label] = {
            "avg_throughput_kbps": round(avg_rate * 8, 2),
            "avg_delay_ms": round(random.uniform(200, 900) * congestion_factor, 1),
            "avg_jitter_ms": round(random.uniform(50, 300), 1),
            "packet_loss_pct": round(random.uniform(3, 12), 2),
            "count": len(pkts)
        }
    return results

def simulate_with_qos(rows, qos_policy):
    """
    Simulates network behavior WITH QoS applied.
    High-priority flows get bandwidth guarantees, lower-priority flows are throttled.
    """
    results = {}

    for label in set(r["classified_label"] for r in rows):
        pkts = [r for r in rows if r["classified_label"] == label]
        if not pkts:
            continue
        policy = qos_policy.get(label, qos_policy["background"])
        avg_rate = sum(float(p["traffic_rate"]) for p in pkts) / len(pkts)

        # High-priority classes get near-ideal performance
        priority = policy["priority_level"]
        delay_factor = 0.1 + (priority * 0.05)  # Lower priority = more delay
        jitter_factor = 0.1 + (priority * 0.04)
        loss_factor = max(0.1, priority * 0.3)

        results[label] = {
            "avg_throughput_kbps": round(avg_rate * 8 * random.uniform(0.9, 1.0), 2),
            "avg_delay_ms": round(policy["max_delay_ms"] * delay_factor * random.uniform(0.4, 0.85), 1),
            "avg_jitter_ms": round(policy["max_jitter_ms"] * jitter_factor * random.uniform(0.2, 0.7), 1),
            "packet_loss_pct": round(loss_factor * random.uniform(0.1, 0.8), 2),
            "count": len(pkts)
        }
    return results

def evaluate_performance(input_path="data/qos_recommended.csv", output_path="data/performance_report.csv"):
    """
    Runs before/after comparison of network performance metrics.
    """
    from modules.qos_recommendation import QOS_POLICY

    print(f"[*] Evaluating performance from '{input_path}'...")
    rows = []
    with open(input_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    before = simulate_without_qos(rows)
    after = simulate_with_qos(rows, QOS_POLICY)

    # Bandwidth utilization per class
    all_labels = sorted(set(list(before.keys()) + list(after.keys())))
    report_rows = []
    for label in all_labels:
        b = before.get(label, {})
        a = after.get(label, {})
        delay_improvement = round(b.get("avg_delay_ms", 0) - a.get("avg_delay_ms", 0), 1)
        jitter_improvement = round(b.get("avg_jitter_ms", 0) - a.get("avg_jitter_ms", 0), 1)
        loss_improvement = round(b.get("packet_loss_pct", 0) - a.get("packet_loss_pct", 0), 2)
        report_rows.append({
            "traffic_class": label,
            "packet_count": b.get("count", 0),
            "before_throughput_kbps": b.get("avg_throughput_kbps", 0),
            "after_throughput_kbps": a.get("avg_throughput_kbps", 0),
            "before_delay_ms": b.get("avg_delay_ms", 0),
            "after_delay_ms": a.get("avg_delay_ms", 0),
            "delay_improvement_ms": delay_improvement,
            "before_jitter_ms": b.get("avg_jitter_ms", 0),
            "after_jitter_ms": a.get("avg_jitter_ms", 0),
            "jitter_improvement_ms": jitter_improvement,
            "before_packet_loss_pct": b.get("packet_loss_pct", 0),
            "after_packet_loss_pct": a.get("packet_loss_pct", 0),
            "loss_improvement_pct": loss_improvement
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(report_rows[0].keys()))
        writer.writeheader()
        writer.writerows(report_rows)

    print(f"[+] Performance report saved to '{output_path}'")
    print("\n    === Performance Summary (Before vs After QoS) ===")
    print(f"    {'Class':<15} {'Delay Before':>14} {'Delay After':>12} {'Improvement':>12}")
    print("    " + "-" * 56)
    for r in report_rows:
        print(f"    {r['traffic_class']:<15} {r['before_delay_ms']:>12.1f}ms {r['after_delay_ms']:>10.1f}ms {r['delay_improvement_ms']:>+10.1f}ms")

    return output_path, report_rows, before, after
