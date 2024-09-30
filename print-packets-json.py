import meshtastic.serial_interface
from pubsub import pub
import json
import time

interface = meshtastic.serial_interface.SerialInterface()

def onReceive(packet, interface):
    packet = json.dumps(packet, indent=2, default=lambda s: " ".join(str(s).split()))
    print(f"{packet} \n\n")

pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    time.sleep(1)