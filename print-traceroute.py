import meshtastic.serial_interface
from pubsub import pub
import time

interface = meshtastic.serial_interface.SerialInterface()
local_node_id = interface.getNode('^local').nodeNum

def onReceive(packet, interface):
    if 'decoded' in packet and packet['decoded']['portnum'] == 'TRACEROUTE_APP':

        message = f"{packet['from']} --> "
        route = packet['decoded']['traceroute'].get('route', [])
        route_str = ' -> '.join(map(str, route))
        message += f"{route_str} --> {packet['to']}"
        print(message)

pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    time.sleep(1)
