import meshtastic.serial_interface
from pubsub import pub
import json

interface = meshtastic.serial_interface.SerialInterface()

def stripnl(s) -> str:
    return " ".join(str(s).split())

def clean_packet(packet):
    if 'decoded' in packet and 'telemetry' in packet['decoded'] and 'raw' in packet['decoded']['telemetry']:
        packet['decoded']['telemetry']['raw'] = stripnl(packet['decoded']['telemetry']['raw'])
    if 'raw' in packet:
        packet['raw'] = stripnl(packet['raw'])
    return packet

def onReceive(packet, interface):
    packet = clean_packet(packet)
    packetJSON = json.dumps(packet, indent=2, default=str)
    print(f"{packetJSON} \n\n")

pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    pass
