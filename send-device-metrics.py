try:
    from meshtastic.protobuf import portnums_pb2, telemetry_pb2
    from meshtastic import BROADCAST_NUM
except ImportError:
    from meshtastic import portnums_pb2, telemetry_pb2, BROADCAST_NUM

# For connection over serial
import meshtastic.serial_interface
interface = meshtastic.serial_interface.SerialInterface()

# For connection over TCP
# import meshtastic.tcp_interface
# interface = meshtastic.tcp_interface.TCPInterface(hostname='192.168.1.42', noProto=False)

telemetry_data = telemetry_pb2.Telemetry()
telemetry_data.device_metrics.battery_level = 69
telemetry_data.device_metrics.voltage = 4.1
telemetry_data.device_metrics.channel_utilization = 42
telemetry_data.device_metrics.air_util_tx = 1

interface.sendData(
    telemetry_data,
    destinationId=BROADCAST_NUM,
    portNum=portnums_pb2.PortNum.TELEMETRY_APP,
    wantResponse=False,
    onResponse=False,
)

interface.close()