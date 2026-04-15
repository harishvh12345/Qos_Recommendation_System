"""
Module 6: Visualization and Reporting Module
NullRoute - Intelligent Network Traffic Classification and QoS System
"""

import csv
import os
from collections import Counter, defaultdict

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("[!] matplotlib not available, skipping chart generation.")

COLORS = {
    "voip": "#FF4757",
    "multimedia": "#FFA502",
    "gaming": "#ECCC68",
    "web": "#2ED573",
    "file_transfer": "#1E90FF",
    "background": "#747D8C"
}

def _save(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, bbox_inches="tight", dpi=150, facecolor="#0F0F1A")
    plt.close(fig)
    print(f"    Saved: {path}")

def plot_traffic_distribution(classified_path, reports_dir="reports"):
    if not HAS_MPL:
        return
    rows = []
    with open(classified_path) as f:
        rows = list(csv.DictReader(f))
    counts = Counter(r["classified_label"] for r in rows)
    labels = list(counts.keys())
    sizes = list(counts.values())
    colors = [COLORS.get(l, "#888") for l in labels]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="#0F0F1A")

    # Pie chart
    ax = axes[0]
    ax.set_facecolor("#0F0F1A")
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.1f%%",
        startangle=140, pctdistance=0.75,
        wedgeprops=dict(edgecolor="#0F0F1A", linewidth=2)
    )
    for t in texts:
        t.set_color("white"); t.set_fontsize(10)
    for a in autotexts:
        a.set_color("white"); a.set_fontsize(9)
    ax.set_title("Traffic Distribution by Category", color="white", fontsize=13, pad=16)

    # Bar chart
    ax2 = axes[1]
    ax2.set_facecolor("#0F0F1A")
    bars = ax2.bar(labels, sizes, color=colors, edgecolor="#0F0F1A", linewidth=1.5)
    for bar, count in zip(bars, sizes):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 str(count), ha="center", va="bottom", color="white", fontsize=9)
    ax2.set_facecolor("#1A1A2E")
    ax2.tick_params(colors="white", labelsize=9)
    ax2.spines[:].set_color("#333")
    ax2.set_ylabel("Packet Count", color="white")
    ax2.set_title("Packets per Traffic Class", color="white", fontsize=13)
    ax2.yaxis.label.set_color("white")

    plt.tight_layout()
    _save(fig, f"{reports_dir}/01_traffic_distribution.png")

def plot_classification_accuracy(classified_path, reports_dir="reports"):
    if not HAS_MPL:
        return
    rows = []
    with open(classified_path) as f:
        rows = list(csv.DictReader(f))
    per_class = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in rows:
        lbl = r["true_label"]
        per_class[lbl]["total"] += 1
        if r["is_correct"] == "YES":
            per_class[lbl]["correct"] += 1

    classes = list(per_class.keys())
    accuracies = [100 * per_class[c]["correct"] / per_class[c]["total"] for c in classes]
    colors = [COLORS.get(c, "#888") for c in classes]

    fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0F0F1A")
    ax.set_facecolor("#1A1A2E")
    bars = ax.barh(classes, accuracies, color=colors, edgecolor="#0F0F1A")
    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{acc:.1f}%", va="center", color="white", fontsize=10)
    ax.axvline(x=100, color="#555", linestyle="--", linewidth=1)
    ax.set_xlim(0, 115)
    ax.set_xlabel("Accuracy (%)", color="white")
    ax.set_title("Classification Accuracy per Traffic Class", color="white", fontsize=13)
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#333")
    plt.tight_layout()
    _save(fig, f"{reports_dir}/02_classification_accuracy.png")

def plot_qos_priorities(qos_path, qos_policy, reports_dir="reports"):
    if not HAS_MPL:
        return
    rows = []
    with open(qos_path) as f:
        rows = list(csv.DictReader(f))
    counts = Counter(r["classified_label"] for r in rows)

    labels = list(qos_policy.keys())
    priorities = [qos_policy[l]["priority_level"] for l in labels]
    dscp_vals = [qos_policy[l]["dscp_value"] for l in labels]
    colors = [qos_policy[l]["color"] for l in labels]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor="#0F0F1A")

    # Priority levels
    ax = axes[0]
    ax.set_facecolor("#1A1A2E")
    bars = ax.bar(labels, [7 - p for p in priorities], color=colors, edgecolor="#0F0F1A")
    for bar, lbl, p in zip(bars, labels, priorities):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"P{p}", ha="center", va="bottom", color="white", fontsize=10, fontweight="bold")
    ax.set_facecolor("#1A1A2E")
    ax.tick_params(colors="white", labelsize=9)
    ax.spines[:].set_color("#333")
    ax.set_ylabel("Relative Priority (Higher=Better)", color="white")
    ax.set_title("QoS Priority Levels per Traffic Class", color="white", fontsize=12)

    # DSCP values
    ax2 = axes[1]
    ax2.set_facecolor("#1A1A2E")
    bars2 = ax2.bar(labels, dscp_vals, color=colors, edgecolor="#0F0F1A")
    for bar, val in zip(bars2, dscp_vals):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 str(val), ha="center", va="bottom", color="white", fontsize=10)
    ax2.tick_params(colors="white", labelsize=9)
    ax2.spines[:].set_color("#333")
    ax2.set_ylabel("DSCP Value (RFC 4594)", color="white")
    ax2.set_title("DSCP Marking per Traffic Class", color="white", fontsize=12)

    plt.tight_layout()
    _save(fig, f"{reports_dir}/03_qos_priorities_dscp.png")

def plot_performance_comparison(report_rows, reports_dir="reports"):
    if not HAS_MPL:
        return
    classes = [r["traffic_class"] for r in report_rows]
    colors = [COLORS.get(c, "#888") for c in classes]
    x = np.arange(len(classes))
    width = 0.35

    metrics = [
        ("avg_delay_ms", "before_delay_ms", "after_delay_ms", "End-to-End Delay (ms)", "01"),
        ("avg_jitter_ms", "before_jitter_ms", "after_jitter_ms", "Jitter (ms)", "02"),
        ("packet_loss_pct", "before_packet_loss_pct", "after_packet_loss_pct", "Packet Loss (%)", "03"),
    ]

    for key, before_key, after_key, ylabel, num in metrics:
        fig, ax = plt.subplots(figsize=(12, 5), facecolor="#0F0F1A")
        ax.set_facecolor("#1A1A2E")
        before_vals = [float(r[before_key]) for r in report_rows]
        after_vals = [float(r[after_key]) for r in report_rows]
        b1 = ax.bar(x - width/2, before_vals, width, label="Without QoS", color="#555577", alpha=0.9)
        b2 = ax.bar(x + width/2, after_vals, width, label="With QoS", color=colors, alpha=0.95)
        ax.set_xticks(x)
        ax.set_xticklabels(classes, color="white", fontsize=10)
        ax.tick_params(colors="white")
        ax.spines[:].set_color("#333")
        ax.set_ylabel(ylabel, color="white")
        ax.set_title(f"{ylabel}: Before vs After QoS", color="white", fontsize=13)
        ax.legend(facecolor="#222", edgecolor="#555", labelcolor="white")
        plt.tight_layout()
        _save(fig, f"{reports_dir}/04_{num}_perf_{key}.png")

def plot_bandwidth_utilization(qos_path, reports_dir="reports"):
    if not HAS_MPL:
        return
    rows = []
    with open(qos_path) as f:
        rows = list(csv.DictReader(f))
    bw_by_class = defaultdict(float)
    for r in rows:
        bw_by_class[r["classified_label"]] += float(r["traffic_rate"]) * float(r["packet_size"]) / 1e6
    classes = list(bw_by_class.keys())
    bw_vals = [bw_by_class[c] for c in classes]
    colors = [COLORS.get(c, "#888") for c in classes]
    fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0F0F1A")
    ax.set_facecolor("#1A1A2E")
    bars = ax.bar(classes, bw_vals, color=colors, edgecolor="#0F0F1A")
    for bar, v in zip(bars, bw_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f"{v:.2f}", ha="center", va="bottom", color="white", fontsize=9)
    ax.tick_params(colors="white", labelsize=9)
    ax.spines[:].set_color("#333")
    ax.set_ylabel("Bandwidth Consumed (MB equivalent)", color="white")
    ax.set_title("Bandwidth Utilization by Traffic Class", color="white", fontsize=13)
    plt.tight_layout()
    _save(fig, f"{reports_dir}/05_bandwidth_utilization.png")

def generate_text_report(classified_path, qos_path, report_rows, accuracy, qos_policy, reports_dir="reports"):
    """Generates a human-readable summary report."""
    from collections import Counter
    rows = []
    with open(classified_path) as f:
        rows = list(csv.DictReader(f))
    counts = Counter(r["classified_label"] for r in rows)
    total = len(rows)
    os.makedirs(reports_dir, exist_ok=True)
    path = f"{reports_dir}/summary_report.txt"
    with open(path, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("  NULLROUTE - INTELLIGENT NETWORK TRAFFIC CLASSIFICATION\n")
        f.write("  AND QoS RECOMMENDATION SYSTEM - SUMMARY REPORT\n")
        f.write("=" * 70 + "\n")
        f.write("  MACSE513 - Computer Networks | School of Computer Science\n")
        f.write("  Team: Vishal (25MAI1003), Vishwa J (25MAI1004), Harish V (25MAI1019)\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"  Total Packets Analyzed : {total}\n")
        f.write(f"  Classification Accuracy: {accuracy}%\n\n")
        f.write("  TRAFFIC DISTRIBUTION:\n")
        f.write("  " + "-" * 50 + "\n")
        for label, count in sorted(counts.items(), key=lambda x: -x[1]):
            pct = 100 * count / total
            policy = qos_policy[label]
            f.write(f"  {label:<16} {count:>5} pkts ({pct:5.1f}%) | DSCP={policy['dscp_value']:>2} | {policy['priority_name']}\n")
        f.write("\n  QoS POLICY SUMMARY (per RFC 4594 / IEEE 802.1p):\n")
        f.write("  " + "-" * 50 + "\n")
        for label, policy in sorted(qos_policy.items(), key=lambda x: x[1]["priority_level"]):
            f.write(f"\n  [{policy['priority_name']}] {label.upper()}\n")
            f.write(f"    DSCP     : {policy['dscp_value']} ({policy['dscp_name']})\n")
            f.write(f"    IEEE 802 : {policy['ieee_priority']}\n")
            f.write(f"    Sched    : {policy['scheduling']}\n")
            f.write(f"    BW Guar  : {policy['bandwidth_guarantee']}\n")
            f.write(f"    Max Delay: {policy['max_delay_ms']} ms\n")
            f.write(f"    Rationale: {policy['rationale']}\n")
        f.write("\n  PERFORMANCE COMPARISON (Before vs After QoS):\n")
        f.write("  " + "-" * 50 + "\n")
        f.write(f"  {'Class':<14} {'Delay Before':>13} {'Delay After':>11} {'Improvement':>12}\n")
        f.write("  " + "-" * 50 + "\n")
        for r in report_rows:
            f.write(f"  {r['traffic_class']:<14} {float(r['before_delay_ms']):>11.1f}ms"
                    f" {float(r['after_delay_ms']):>9.1f}ms {float(r['delay_improvement_ms']):>+10.1f}ms\n")
        f.write("\n" + "=" * 70 + "\n")
        f.write("  CONCEPTS DEMONSTRATED:\n")
        f.write("    TCP/IP Protocol Suite, DiffServ (RFC 2474/4594),\n")
        f.write("    IEEE 802.1p QoS, Flow-Based Traffic Classification,\n")
        f.write("    Bandwidth Utilization, Jitter & Delay Analysis,\n")
        f.write("    Weighted Fair Queuing (WFQ), Priority Queuing (PQ)\n")
        f.write("=" * 70 + "\n")
    print(f"    Report saved: {path}")
    return path

def run_visualization(classified_path, qos_path, report_rows, accuracy, qos_policy, reports_dir="reports"):
    print(f"[*] Generating visualizations...")
    plot_traffic_distribution(classified_path, reports_dir)
    plot_classification_accuracy(classified_path, reports_dir)
    plot_qos_priorities(qos_path, qos_policy, reports_dir)
    plot_performance_comparison(report_rows, reports_dir)
    plot_bandwidth_utilization(qos_path, reports_dir)
    rpt = generate_text_report(classified_path, qos_path, report_rows, accuracy, qos_policy, reports_dir)
    print(f"[+] All visualizations and report generated in '{reports_dir}/'")
