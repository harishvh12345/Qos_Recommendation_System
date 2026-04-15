# NullRoute — Intelligent Network Traffic Classification and QoS Recommendation System
## MACSE513 — Computer Networks | School of Computer Science and Engineering

**Team:** Vishal (25MAI1003) · Vishwa J (25MAI1004) · Harish V (25MAI1019)

---

## Project Structure

```
nullroute/
├── main.py                          ← Run the full pipeline
├── requirements.txt
├── modules/
│   ├── traffic_capture.py           ← Module 1: Packet capture simulation
│   ├── feature_extraction.py        ← Module 2: Feature engineering
│   ├── traffic_classification.py    ← Module 3: Rule-based classifier
│   ├── qos_recommendation.py        ← Module 4: QoS policy engine
│   ├── performance_evaluation.py    ← Module 5: Before/After metrics
│   └── visualization.py             ← Module 6: Charts & reports
├── data/                            ← CSV data files (auto-generated)
├── reports/                         ← Charts + summary report (auto-generated)
└── static/
    └── dashboard.html               ← Interactive project dashboard
```

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline
```bash
python main.py                  # 300 packets (default)
python main.py --packets 500    # custom count
```

### 3. Open the dashboard
Open `static/dashboard.html` in any browser — no server needed.

---

## Modules

| # | Module | Function |
|---|--------|----------|
| 1 | Traffic Capture | Simulates LAN packet capture (Wireshark-style) |
| 2 | Feature Extraction | Derives flow attributes from raw packets |
| 3 | Traffic Classification | Rule-based engine (port + protocol + heuristics) |
| 4 | QoS Recommendation | Applies RFC 4594 / IEEE 802.1p policy |
| 5 | Performance Evaluation | Before/After comparison (delay, jitter, loss) |
| 6 | Visualization | Matplotlib charts + text summary report |

---

## CN Concepts Demonstrated

- **TCP/IP Protocol Suite** — Layer 3/4 packet classification
- **DiffServ (RFC 2474/4594)** — DSCP marking (EF, AF41, AF31, AF11, BE)
- **IEEE 802.1p** — Layer 2 priority tagging (0–7)
- **QoS Scheduling** — Priority Queue, WFQ, DRR, Best Effort
- **Network Performance Metrics** — Throughput, Delay, Jitter, Packet Loss
- **Flow-Based Classification** — 5-tuple flow identification
- **Bandwidth Management** — Per-class bandwidth guarantees

---

## Classification Accuracy: **~95.67%**

## Output Files

After running `main.py`:
- `data/captured_traffic.csv` — raw packet data
- `data/extracted_features.csv` — enriched feature set
- `data/classified_traffic.csv` — classification results
- `data/qos_recommended.csv` — QoS annotations
- `data/performance_report.csv` — metric comparison
- `reports/*.png` — 7 visualization charts
- `reports/summary_report.txt` — human-readable report
