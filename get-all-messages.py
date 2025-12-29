import time
from pubsub import pub
from meshtastic.tcp_interface import TCPInterface
import meshtastic.serial_interface

# interface = TCPInterface(hostname="192.168.86.69")
interface = meshtastic.serial_interface.SerialInterface()

def on_receive(packet, interface):
    try:
        if packet.get("decoded", {}).get("portnum") == "TEXT_MESSAGE_APP":
            msg = packet["decoded"]["payload"].decode()
            print(msg)
    except Exception:
        pass

pub.subscribe(on_receive, "meshtastic.receive")

time.sleep(10)
interface.close()