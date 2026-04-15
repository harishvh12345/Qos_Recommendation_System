from scapy.all import PcapReader, IP, TCP, UDP
import pandas as pd

def extract_features(pcap_file):
    print(f"Reading {pcap_file}... This might take a minute depending on file size.")
    packet_data = []
    
    # Using PcapReader to read packet by packet efficiently
    for pkt in PcapReader(pcap_file):
        # We only care about IP packets for this project
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            size = len(pkt)
            
            # Default values
            src_port = 0
            dst_port = 0
            protocol = 'Other'
            
            # Check if it's TCP
            if TCP in pkt:
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
                protocol = 'TCP'
            # Check if it's UDP
            elif UDP in pkt:
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport
                protocol = 'UDP'
                
            packet_data.append({
                'Source_IP': src_ip,
                'Destination_IP': dst_ip,
                'Source_Port': src_port,
                'Destination_Port': dst_port,
                'Protocol': protocol,
                'Packet_Size': size
            })
            
    # Convert our list of packets into a structured DataFrame
    df = pd.DataFrame(packet_data)
    
    # Save it to a CSV file
    csv_filename = "extracted_traffic.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Success! Extracted {len(df)} packets and saved to {csv_filename}")

# Run the function on your file
extract_features("traffic1.pcap")