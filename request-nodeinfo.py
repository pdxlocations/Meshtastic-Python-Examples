from meshtastic.protobuf import mesh_pb2
import meshtastic.serial_interface
from pubsub import pub
import time
import base64

target_id = 576335798
interface = meshtastic.serial_interface.SerialInterface()

# Build User protobuf from local node info
local_info = interface.getMyNodeInfo()
local_user = mesh_pb2.User()

local_user.id = local_info["user"]["id"]
local_user.long_name = local_info["user"]["longName"]
local_user.short_name = local_info["user"]["shortName"]
local_user.hw_model = local_info["user"]["hwModel"]
public_key_b64 = local_info["user"]["publicKey"]
local_user.public_key = base64.b64decode(public_key_b64)

def onReceive(packet, interface):
    if packet["from"] == target_id:
        print(f"{packet}\n")

pub.subscribe(onReceive, "meshtastic.receive")

interface.sendData(
    local_user,
    destinationId=target_id,
    portNum=meshtastic.portnums_pb2.NODEINFO_APP,
    wantResponse=True,
)

while True:
    time.sleep(1)