
from meshtastic.protobuf import mesh_pb2, config_pb2
from meshtastic import BROADCAST_NUM
import meshtastic.serial_interface

interface = meshtastic.serial_interface.SerialInterface()

user = mesh_pb2.User()
me = interface.nodesByNum[interface.localNode.nodeNum]['user']
user.id = me['id']
user.long_name = me['longName']
user.short_name = me['shortName']
user.hw_model = mesh_pb2.HardwareModel.Value(me['hwModel'])
if user.role:
    user.role = config_pb2.Config.DeviceConfig.Role.Value(me['role'])

interface.sendData(
    user,
    destinationId=BROADCAST_NUM,
    portNum=meshtastic.portnums_pb2.NODEINFO_APP,
    wantAck=False,
    wantResponse=False
)
interface.close()




