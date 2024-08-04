import meshtastic.serial_interface
from pubsub import pub
import json

interface = meshtastic.serial_interface.SerialInterface()

def onReceive(packet, interface):
    packetJSON = json.dumps(packet, indent=2, default=str)
    print(f"{packetJSON} \n\n") 

pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    pass
