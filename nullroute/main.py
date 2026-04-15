"""
NullRoute - Intelligent Network Traffic Classification and QoS Recommendation System
MACSE513 - Computer Networks Project
Team: Vishal (25MAI1003), Vishwa J (25MAI1004), Harish V (25MAI1019)

Main pipeline - runs all 6 modules in sequence.
Usage:
    python main.py              # Default: 300 packets
    python main.py --packets 500
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def banner():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║       NULLROUTE — Network Traffic Classification & QoS          ║
║       MACSE513 Computer Networks | Team: Vishal, Vishwa, Harish  ║
╚══════════════════════════════════════════════════════════════════╝
""")

def run_pipeline(num_packets=300):
    banner()
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base, "data")
    reports_dir = os.path.join(base, "reports")

    # ── Module 1: Capture ──────────────────────────────────────────────────────
    print("━" * 60)
    print(" MODULE 1: Network Traffic Capture")
    print("━" * 60)
    from modules.traffic_capture import capture_traffic
    captured = capture_traffic(
        num_packets=num_packets,
        output_path=os.path.join(data_dir, "captured_traffic.csv")
    )

    # ── Module 2: Feature Extraction ───────────────────────────────────────────
    print("\n" + "━" * 60)
    print(" MODULE 2: Feature Extraction")
    print("━" * 60)
    from modules.feature_extraction import extract_features
    features = extract_features(
        input_path=captured,
        output_path=os.path.join(data_dir, "extracted_features.csv")
    )

    # ── Module 3: Classification ───────────────────────────────────────────────
    print("\n" + "━" * 60)
    print(" MODULE 3: Traffic Classification")
    print("━" * 60)
    from modules.traffic_classification import classify_traffic
    classified, accuracy = classify_traffic(
        input_path=features,
        output_path=os.path.join(data_dir, "classified_traffic.csv")
    )

    # ── Module 4: QoS Recommendation ──────────────────────────────────────────
    print("\n" + "━" * 60)
    print(" MODULE 4: QoS Recommendation")
    print("━" * 60)
    from modules.qos_recommendation import apply_qos
    qos_out, qos_policy = apply_qos(
        input_path=classified,
        output_path=os.path.join(data_dir, "qos_recommended.csv")
    )

    # ── Module 5: Performance Evaluation ──────────────────────────────────────
    print("\n" + "━" * 60)
    print(" MODULE 5: Performance Evaluation")
    print("━" * 60)
    from modules.performance_evaluation import evaluate_performance
    perf_out, report_rows, before, after = evaluate_performance(
        input_path=qos_out,
        output_path=os.path.join(data_dir, "performance_report.csv")
    )

    # ── Module 6: Visualization ────────────────────────────────────────────────
    print("\n" + "━" * 60)
    print(" MODULE 6: Visualization & Reporting")
    print("━" * 60)
    from modules.visualization import run_visualization
    run_visualization(classified, qos_out, report_rows, accuracy, qos_policy, reports_dir)

    print("\n" + "━" * 60)
    print(" ✓ PIPELINE COMPLETE")
    print("━" * 60)
    print(f"   Data files : {data_dir}/")
    print(f"   Charts     : {reports_dir}/")
    print(f"   Accuracy   : {accuracy}%")
    print("━" * 60)

if __name__ == "__main__":
    packets = 300
    if "--packets" in sys.argv:
        idx = sys.argv.index("--packets")
        packets = int(sys.argv[idx + 1])
    run_pipeline(num_packets=packets)
