import meshtastic.serial_interface
import time

message = "Test Message"
sender_node_id = 3718164584

interface = meshtastic.serial_interface.SerialInterface()

def send_message(message):
    interface.sendText(
        text=message,
        destinationId=sender_node_id,
        wantAck=True,
        wantResponse=True
        )

send_message(message)

while True:
    time.sleep(0.1)