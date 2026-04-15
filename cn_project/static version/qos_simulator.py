import pandas as pd

def assign_priority(category):
    # Rule-based QoS Priority Mapping based on application importance
    if category == 'Multimedia Traffic':
        return '1 - High (Delay Sensitive)'
    elif category == 'Web Traffic':
        return '2 - Medium (Interactive)'
    elif category == 'File Transfer':
        return '3 - Low (Throughput Focus)'
    elif category == 'Background Traffic':
        return '4 - Lowest (Best Effort)'
    else:
        return '5 - Default'

def run_qos_simulation():
    print("Loading classified traffic data...")
    # Load the CSV we generated in Sprint 2
    df = pd.read_csv('classified_traffic.csv')

    print("Applying QoS Recommendations...")
    # Create a new column for priority levels
    df['QoS_Priority'] = df['Traffic_Category'].apply(assign_priority)

    # Save the finalized data
    output_file = 'qos_evaluated_traffic.csv'
    df.to_csv(output_file, index=False)
    print(f"Success! QoS data saved to {output_file}\n")

    # Performance Evaluation: Calculating Bandwidth & Packet Stats
    print("--- Performance Evaluation: Simulated Bandwidth Usage ---")
    
    # Group the data to see how many bytes and packets belong to each priority
    traffic_stats = df.groupby(['QoS_Priority', 'Traffic_Category']).agg(
        Total_Packets=('Protocol', 'count'),
        Total_Bytes=('Packet_Size', 'sum')
    ).reset_index()

    # Sort to show High priority at the top
    traffic_stats = traffic_stats.sort_values(by='QoS_Priority')
    
    # Calculate percentage of total bandwidth
    total_network_bytes = traffic_stats['Total_Bytes'].sum()
    traffic_stats['Bandwidth_Percentage'] = (traffic_stats['Total_Bytes'] / total_network_bytes * 100).round(2).astype(str) + '%'

    print(traffic_stats.to_string(index=False))
    print("\n[Recommendation]: In a live router, Priority 1 traffic should be assigned to a Low-Latency Queue (LLQ).")

if __name__ == "__main__":
    run_qos_simulation()