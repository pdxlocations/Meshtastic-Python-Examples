from meshtastic.protobuf import mesh_pb2
import meshtastic.serial_interface
from pubsub import pub
import time

targetid = 1623194643

interface = meshtastic.serial_interface.SerialInterface()
user = mesh_pb2.User()

def onReceive(packet, interface):
    if packet['from'] == targetid:
        print(f"{packet} \n")

pub.subscribe(onReceive, 'meshtastic.receive')

interface.sendData(
    user,
    destinationId=targetid,
    portNum=meshtastic.portnums_pb2.NODEINFO_APP,

    wantResponse=True,
)

while True:
    time.sleep(1)