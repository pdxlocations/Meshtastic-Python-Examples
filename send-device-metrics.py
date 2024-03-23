from meshtastic import portnums_pb2, telemetry_pb2
import meshtastic.serial_interface

interface = meshtastic.serial_interface.SerialInterface()

BROADCAST_ADDR = 4294967295

telemetry_data = telemetry_pb2.Telemetry()
telemetry_data.device_metrics.battery_level = 69
telemetry_data.device_metrics.voltage = 4.2
telemetry_data.device_metrics.channel_utilization = 42
telemetry_data.device_metrics.air_util_tx = 1

interface.sendData(
    telemetry_data,
    destinationId=BROADCAST_ADDR,
    portNum=portnums_pb2.PortNum.TELEMETRY_APP,
    wantResponse=False,
    onResponse=False,
)

interface.close()