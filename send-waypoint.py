
import time
import random
from meshtastic.protobuf import portnums_pb2, mesh_pb2
from meshtastic import BROADCAST_ADDR

import meshtastic.serial_interface
interface = meshtastic.serial_interface.SerialInterface()

def expire_time(delay: int = 30) -> int:
    return int(time.time()) + delay


waypoint = mesh_pb2.Waypoint()
waypoint.latitude_i = 454877655
waypoint.longitude_i = -1215699769
waypoint.id = id=random.randint(1, 2**32 - 1)
waypoint.expire = expire_time(120)
waypoint.locked_to = interface.myInfo.my_node_num
waypoint.name = 'Point 1'
waypoint.description = 'Waypoint 1 with emoji 🔥'
waypoint.icon = 128293

interface.sendData(
    waypoint,
    destinationId=BROADCAST_ADDR,
    portNum=portnums_pb2.PortNum.WAYPOINT_APP,
    wantResponse=False,
)

interface.close()
