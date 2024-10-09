import meshtastic.serial_interface
from pubsub import pub
import time

interface = meshtastic.serial_interface.SerialInterface()

def onReceive(packet, interface):
    if 'decoded' in packet:
        message_bytes = packet['decoded']['payload']
        message_string = message_bytes.decode('utf-8')
        print(message_string)

pub.subscribe(onReceive, 'meshtastic.receive.text')

while True:
    time.sleep(1)