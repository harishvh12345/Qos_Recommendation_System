import pandas as pd

def classify_traffic(row):
    # Check both source and destination ports to catch traffic flowing in either direction
    ports = [row['Source_Port'], row['Destination_Port']]
    proto = row['Protocol']

    # 1. Web Traffic (HTTP: 80, HTTPS: 443, Alternative Web: 8080)
    if 80 in ports or 443 in ports or 8080 in ports:
        return 'Web Traffic'

    # 2. File Transfer (FTP: 20/21, SSH/SFTP: 22)
    elif 20 in ports or 21 in ports or 22 in ports:
        return 'File Transfer'

    # 3. Background Traffic (DNS: 53, NTP: 123)
    elif 53 in ports or 123 in ports:
        return 'Background Traffic'

    # 4. Multimedia Traffic (Streaming often relies on UDP to avoid latency)
    elif proto == 'UDP':
        return 'Multimedia Traffic'

    # 5. Catch-all for anything else
    else:
        return 'Unclassified / Other'

def run_classifier():
    print("Loading extracted traffic data...")
    # Load the CSV we generated in Sprint 1
    df = pd.read_csv('extracted_traffic.csv')

    print("Applying intelligent rule-based logic...")
    # Create a new column and apply our rules to every single packet
    df['Traffic_Category'] = df.apply(classify_traffic, axis=1)

    # Save the updated data to a new file
    output_file = 'classified_traffic.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\nSuccess! Classified data saved to {output_file}")
    
    # Print a quick summary to the terminal so we can see the results instantly
    print("\n--- Classification Breakdown ---")
    print(df['Traffic_Category'].value_counts())

# Execute the script
if __name__ == "__main__":
    run_classifier()