import meshtastic.serial_interface
from pubsub import pub

interface = meshtastic.serial_interface.SerialInterface()

def onReceive(packet, interface):
    message_bytes = packet['decoded']['payload']
    message_string = message_bytes.decode('utf-8')
    print(message_string)

pub.subscribe(onReceive, 'meshtastic.receive.text')

while True:
    pass