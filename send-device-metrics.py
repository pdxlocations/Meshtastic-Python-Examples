from meshtastic.protobuf import portnums_pb2, telemetry_pb2
from meshtastic import BROADCAST_NUM

import time

# For connection over serial
import meshtastic.serial_interface
interface = meshtastic.serial_interface.SerialInterface()

# For connection over TCP
# import meshtastic.tcp_interface
# interface = meshtastic.tcp_interface.TCPInterface(hostname='192.168.1.42')

telemetry_data = telemetry_pb2.Telemetry()
telemetry_data.device_metrics.battery_level = 69
telemetry_data.device_metrics.voltage = 4.1
telemetry_data.device_metrics.channel_utilization = 42
telemetry_data.device_metrics.air_util_tx = 1
telemetry_data.time = int(time.time())

interface.sendData(
    telemetry_data,
    destinationId=BROADCAST_NUM,
    portNum=portnums_pb2.TELEMETRY_APP,
    wantResponse=False,
    onResponse=False,
)

interface.close()