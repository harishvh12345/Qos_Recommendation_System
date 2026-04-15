import pandas as pd
import matplotlib.pyplot as plt

def generate_dashboard():
    print("Loading QoS evaluated data...")
    # Load the final CSV from Sprint 3
    df = pd.read_csv('qos_evaluated_traffic.csv')

    # Set up a wide figure to hold 3 graphs side-by-side
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('NullRoute: Intelligent Network Traffic & QoS Dashboard', fontsize=16, fontweight='bold')

    # --- Graph 1: Traffic Category Distribution (Pie Chart) ---
    category_counts = df['Traffic_Category'].value_counts()
    axes[0].pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
    axes[0].set_title('Traffic Category Distribution')

    # --- Graph 2: Bandwidth Usage by QoS Priority (Bar Chart) ---
    # Summing up the 'Packet_Size' (bytes) for each priority level
    priority_bytes = df.groupby('QoS_Priority')['Packet_Size'].sum()
    # Convert to Kilobytes for easier reading
    priority_kb = priority_bytes / 1024 
    priority_kb.plot(kind='bar', ax=axes[1], color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'])
    axes[1].set_title('Simulated Bandwidth Usage by QoS')
    axes[1].set_ylabel('Total Kilobytes (KB)')
    axes[1].set_xlabel('Assigned Priority Level')
    axes[1].tick_params(axis='x', rotation=45)

    # --- Graph 3: Protocol Distribution (Pie Chart) ---
    protocol_counts = df['Protocol'].value_counts()
    axes[2].pie(protocol_counts, labels=protocol_counts.index, autopct='%1.1f%%', startangle=90, colors=['#9467bd', '#8c564b', '#e377c2'])
    axes[2].set_title('Protocol Breakdown')

    # Adjust layout so labels don't overlap
    plt.tight_layout()
    
    # Save a high-resolution copy for your final project report
    print("Saving dashboard image as 'final_dashboard.png'...")
    plt.savefig('final_dashboard.png', dpi=300)
    
    # Pop open the interactive window
    print("Launching dashboard...")
    plt.show()

if __name__ == "__main__":
    generate_dashboard()