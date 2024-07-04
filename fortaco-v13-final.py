import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load logs into a DataFrame
df = pd.read_csv('RWC_6_logs.csv', header=None, names=['timestamp', 'success', 'host', 'ip', 'packetsize', 'rtt', 'ttl'])

# Convert 'timestamp' to datetime with specified format
df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601', utc=True, errors='coerce')

# Convert 'success' to boolean
df['success'] = df['success'].astype(str).str.lower() == 'true'

# Modify timestamp to match the correct timezone
df['timestamp'] = df['timestamp'].dt.tz_convert('Europe/Helsinki')

# Function to extract RTT value
def extract_rtt(row):
    if row['success']:
        try:
            return float(row['rtt'].replace('ms', ''))
        except (ValueError, AttributeError):
            return np.nan
    return 0.1  # Return 0.1 for failed pings instead of 0

# Apply the function to create a new 'rtt_value' column
df['rtt_value'] = df.apply(extract_rtt, axis=1)

# Sort DataFrame by timestamp
df = df.sort_values('timestamp')

# Calculate rolling averages separately for success and failure
rolling_window = 600  # Adjust this value to change the smoothness of the rolling average
df['rolling_avg_success'] = df[df['success']]['rtt_value'].rolling(window=rolling_window, center=True).mean()
df['rolling_avg_failure'] = df[~df['success']]['rtt_value'].rolling(window=rolling_window, center=True).mean()

# Calculate overall average RTT
average_rtt = df[df['success']]['rtt_value'].mean()

# Function to create tick values and labels
def create_ticks(max_power):
    tick_values = [0.1] + [10**i for i in range(0, max_power + 1)]
    tick_labels = ['0'] + [f'10^{i}' for i in range(0, max_power + 1)]
    return tick_values, tick_labels
 
# Adjust this value to change the number of tick values
max_power = 4  # This will create ticks: 0.1, 1, 10, 100, 1000, 10000

tick_values, tick_labels = create_ticks(max_power)

# Create the plot
fig = go.Figure()

# Create separate DataFrames for successful and failed pings
df_success = df[df['success']]
df_failure = df[~df['success']]

df_success_avg = df_success.groupby('timestamp')['rtt_value'].mean().reset_index()

# Add scatter plot for successful pings (averaged)
fig.add_trace(go.Scatter(
    x=df_success_avg['timestamp'],
    y=df_success_avg['rtt_value'],
    mode='markers',
    name='Success',
    marker=dict(color='blue', size=5),
    hovertemplate='RTT: %{y:.2f} ms<br>Timestamp: %{x}<extra></extra>'
))

# Add scatter plot for failed pings
fig.add_trace(go.Scatter(
    x=df_failure['timestamp'],
    y=[0.1] * len(df_failure),  # Use 0.1 to make failures visible on log scale
    mode='markers',
    name='Failure',
    marker=dict(color='red', size=5),
    hovertemplate='Failure<br>Timestamp: %{x}<extra></extra>'
))

# Add rolling average line for successful pings
fig.add_trace(go.Scatter(
    x=df['timestamp'],
    y=df['rolling_avg_success'].combine_first(df['timestamp'].map(lambda x: average_rtt)),
    mode='lines',
    name=f'Rolling Avg (Success, window={rolling_window})',
    line=dict(color='green', width=2),
    hovertemplate='Rolling Avg RTT: %{y:.2f} ms<br>Timestamp: %{x}<extra></extra>',
    hoverlabel=dict(namelength=0)
))

# Add rolling average line for failed pings
fig.add_trace(go.Scatter(
    x=df['timestamp'],
    y=df['rolling_avg_failure'],
    mode='lines',
    name=f'Rolling Avg (Failure, window={rolling_window})',
    line=dict(color='purple', width=3),
    hovertemplate='Rolling Avg RTT: Failed Ping! (0ms)<br>Timestamp: %{x}<extra></extra>'
))

# Add average RTT line
fig.add_trace(go.Scatter(
    x=[df['timestamp'].min(), df['timestamp'].max()],
    y=[average_rtt] * 2,
    mode='lines',
    name=f'Average RTT: {average_rtt:.2f} ms',
    line=dict(color="orange", width=2, dash="dash"),
    hovertemplate='Average RTT: %{y:.2f} ms<br>Timestamp: %{x}<extra></extra>'
))

# Update layout with logarithmic Y-axis
fig.update_layout(
    title='Ping Results / Fortaco v13',
    xaxis_title='Timestamp',
    yaxis_title='RTT (ms)',
    yaxis=dict(
        type='log',
        tickmode='array',
        tickvals=tick_values,
        ticktext=tick_labels,
        range=[np.log10(0.1), np.log10(10**max_power)]
    ),
    showlegend=True
)

# Show the plot
fig.show()