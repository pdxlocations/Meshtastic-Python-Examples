import meshtastic.serial_interface
from pubsub import pub
import time

iface = meshtastic.serial_interface.SerialInterface()
ourNum = iface.getNode("^local").nodeNum

def onReceive(packet, interface):
    ls = packet.get("decoded", {}).get("telemetry", {}).get("localStats")
    if packet.get("from") == ourNum and ls:
        print("LOCAL STATS:")
        for k, v in ls.items():
            print(f"  {k:20} : {v}")

pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)