import meshtastic.serial_interface
from pubsub import pub
import json
import time
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import Counter

interface = meshtastic.serial_interface.SerialInterface()
local_node_id = interface.getNode('^local').nodeNum
file_path = 'received_data.json'

def onReceive(packet, interface):

    if packet['from'] != local_node_id:
        json_packet = json.dumps(packet, indent=2, default=lambda s: " ".join(str(s).split()))

        # Read the existing content and update it
        if os.path.exists(file_path):
            with open(file_path, 'r+') as json_file:
                content = json_file.read().strip()
                if content:
                    if content.endswith(']'):
                        content = content[:-1].rstrip() + ',\n'
                    else:
                        content = '['
                    json_file.seek(0)
                    json_file.write(content + json_packet + '\n]')
                else:
                    json_file.seek(0)
                    json_file.write('[' + json_packet + '\n]')
                json_file.truncate()
        else:
            with open(file_path, 'w') as json_file:
                json_file.write('[\n' + json_packet + '\n]')

        print(f"Received and saved packet:\n{json_packet}\n\n")

pub.subscribe(onReceive, 'meshtastic.receive')

def update_plots(frame):
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            
            # Extract 'portnum' values, count occurrences
            portnums = [item.get('decoded', {}).get('portnum', 'Unknown') for item in data]
            portnum_counts = Counter(portnums)
            
            # Extract 'from' values, count occurrences
            from_values = [item.get('from', 'Unknown') for item in data]
            from_counts = Counter(from_values)
            
            # Plot portnum counts
            ax1.clear()
            ax1.bar(portnum_counts.keys(), portnum_counts.values(), color='b', label='Portnums')
            # ax1.set_xlabel('Portnums')
            ax1.set_ylabel('Count')
            ax1.set_title('Portnums Frequency')
            ax1.legend()
            ax1.tick_params(axis='x', rotation=90)  # Rotate x-axis labels to vertical
            
            # Plot from counts
            ax2.clear()
            from_counts_str = {str(key): value for key, value in from_counts.items()}
            ax2.bar(from_counts_str.keys(), from_counts_str.values(), color='r', label='From Numbers')
            # ax2.set_xlabel('From Numbers')
            ax2.set_ylabel('Count')
            ax2.set_title('From Numbers Frequency')
            ax2.legend()
            ax2.tick_params(axis='x', rotation=90)  # Rotate x-axis labels to vertical

# Set up the plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
plt.subplots_adjust(bottom=0.2)
ani = FuncAnimation(fig, update_plots, interval=1000)
plt.show()

while True:
    time.sleep(1)
