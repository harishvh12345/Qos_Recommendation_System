import streamlit as st
import pandas as pd
import plotly.express as px
import time
import pandas.errors

# Set up the webpage
st.set_page_config(page_title="QoS Intelligence Dashboard",page_icon="computer-vision.png", layout="wide")
#st.title("🌐 Real-Time Traffic & QoS Intelligence")
# Create two columns: a small one for the logo (1 part), a large one for the title (10 parts)
logo_col, title_col = st.columns([1, 20])

with logo_col:
    # Replace 'your_icon.png' with the exact name of your Flaticon file!
    st.image("computer-vision.png", width=80) 

with title_col:
    # Notice we removed the globe emoji here
    st.title("NullRoute: Real-Time Traffic & QoS Intelligence")
st.markdown("Live tracking of local network traffic, intelligent QoS classification, and destination mapping.")

# Create a placeholder that we will constantly overwrite with new data
placeholder = st.empty()

# Run a continuous loop to update the dashboard
while True:
    try:
        # Try to read the live data file
        df = pd.read_csv('live_traffic.csv')
        
        with placeholder.container():
            # Top Row: Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Packets Captured", len(df))
            col2.metric("Total Bandwidth (KB)", round(df['Size'].sum() / 1024, 2))
            col3.metric("Active Connections", df['Destination'].nunique())
            
            st.markdown("---")
            
            # Middle Row: Charts
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.subheader("Traffic Category Distribution")
                fig_pie = px.pie(df, names='Category', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                # Add a unique key using time.time()
                st.plotly_chart(fig_pie, use_container_width=True, key=f"pie_{time.time()}") 
                            
            with chart_col2:
                st.subheader("Bandwidth Usage by QoS Priority")
                qos_data = df.groupby('QoS')['Size'].sum().reset_index()
                fig_bar = px.bar(qos_data, x='QoS', y='Size', color='QoS', labels={'Size': 'Bytes'})
                # Add a unique key here too
                st.plotly_chart(fig_bar, use_container_width=True, key=f"bar_{time.time()}")

            st.markdown("---")
            
            # Bottom Row: Geo-IP Mapping
            st.subheader("Live Destination Map")
            # Filter out local IPs that don't have lat/lon
            map_data = df.dropna(subset=['latitude', 'longitude'])
            if not map_data.empty:
                st.map(map_data)
            else:
                st.info("Waiting for external web traffic to map coordinates...")
                
    except FileNotFoundError:
        st.warning("Waiting for live_sniffer.py to start capturing data...")
    except pandas.errors.EmptyDataError:
        # If the file is mid-write and temporarily empty, just skip and wait
        pass
    except Exception as e:
        # Catch any other random file lock errors safely
        pass
    # Wait 2 seconds before refreshing the dashboard
    time.sleep(2)