import meshtastic.serial_interface
from pubsub import pub
import json
import time
import os

interface = meshtastic.serial_interface.SerialInterface()
local_node_id = interface.getNode('^local')
file_path = 'received_data.json'

def onReceive(packet, interface):
    if packet['from'] is not local_node_id:
        json_packet = json.dumps(packet, indent=4, default=lambda s: " ".join(str(s).split()))
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

        print(f"{json_packet}\n\n")

pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    time.sleep(1)
