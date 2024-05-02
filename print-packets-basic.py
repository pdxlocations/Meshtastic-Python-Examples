import meshtastic.serial_interface
from pubsub import pub

interface = meshtastic.serial_interface.SerialInterface()

def onReceive(packet, interface):
    print(f"{packet} \n\n") 

pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    pass
