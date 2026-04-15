import os

print("--- Starting NullRoute Traffic System ---")
print("\n[1/4] Extracting Features from PCAP...")
os.system("python extractor.py")

print("\n[2/4] Classifying Traffic...")
os.system("python classifier.py")

print("\n[3/4] Running QoS Simulation...")
os.system("python qos_simulator.py")

print("\n[4/4] Generating Dashboard...")
os.system("python visualizer.py")

print("\n--- Demo Complete ---")