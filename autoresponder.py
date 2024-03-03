import meshtastic.serial_interface
from pubsub import pub

reply_message = "Message Received"

interface = meshtastic.serial_interface.SerialInterface()
def onReceive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            print(f"Received: {message_string}")
            send_message(reply_message)

    except KeyError as e:
        print(f"Error processing packet: {e}")

pub.subscribe(onReceive, 'meshtastic.receive')

def send_message(message):
    interface.sendText(message)
    print (f"Sent: {reply_message}")

while True:
    pass