from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import requests
import os

print("--- NullRoute Live Sniffer Started ---")
print("Listening for network traffic... (Press Ctrl+C to stop)")

# Cache to store IP locations so we don't hit API rate limits
ip_cache = {}
live_data = []

def get_geo_location(ip_address):
    # Ignore local/private network IPs
    if ip_address.startswith(('192.168.', '10.', '127.', '172.')):
        return None, None
    
    # Check if we already looked up this IP
    if ip_address in ip_cache:
        return ip_cache[ip_address]
        
    try:
        # Free API to get Latitude and Longitude
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=2).json()
        if response['status'] == 'success':
            lat, lon = response['lat'], response['lon']
            ip_cache[ip_address] = (lat, lon)
            return lat, lon
    except:
        pass
    
    ip_cache[ip_address] = (None, None)
    return None, None

def process_packet(pkt):
    if IP in pkt:
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        size = len(pkt)
        
        src_port, dst_port, protocol = 0, 0, 'Other'
        if TCP in pkt:
            src_port, dst_port, protocol = pkt[TCP].sport, pkt[TCP].dport, 'TCP'
        elif UDP in pkt:
            src_port, dst_port, protocol = pkt[UDP].sport, pkt[UDP].dport, 'UDP'
            
        # 1. Classify Logic (UPDATED for Modern Streaming)
        ports = [src_port, dst_port]
        
        # Check Background first (DNS: 53, NTP: 123)
        if 53 in ports or 123 in ports:
            category = 'Background Traffic'
            qos = '4 - Lowest'
            
        # Check File Transfer (FTP: 20/21, SSH: 22)
        elif 20 in ports or 21 in ports or 22 in ports:
            category = 'File Transfer'
            qos = '3 - Low'
            
        # Check Multimedia (Any UDP that isn't DNS/NTP, this catches YouTube's QUIC protocol)
        elif protocol == 'UDP':
            category = 'Multimedia Traffic'
            qos = '1 - High'
            
        # Check Web Traffic (TCP 80, 443, 8080)
        elif 80 in ports or 443 in ports or 8080 in ports:
            category = 'Web Traffic'
            qos = '2 - Medium'
            
        else:
            category = 'Other'
            qos = '5 - Default'

        # 2. Geo-Location (Track where the destination server is)
        lat, lon = get_geo_location(dst_ip)

        # 3. Save Data
        packet_info = {
            'Source': src_ip, 'Destination': dst_ip, 'Protocol': protocol, 
            'Size': size, 'Category': category, 'QoS': qos,
            'latitude': lat, 'longitude': lon  # Streamlit looks for exactly 'latitude' and 'longitude'
        }
        
        live_data.append(packet_info)
        
        # Save to CSV every 10 packets to keep the dashboard updated
        if len(live_data) % 10 == 0:
            df = pd.DataFrame(live_data)
            df.to_csv('live_traffic.csv', index=False)
            print(f"Captured {len(live_data)} packets...")

# Start sniffing (adjust 'count' to 0 for infinite)
sniff(prn=process_packet, store=False, count=0)
print("Capture complete. Data saved to live_traffic.csv")