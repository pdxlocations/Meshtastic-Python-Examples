from meshtastic import portnums_pb2, telemetry_pb2
import meshtastic.serial_interface

interface = meshtastic.serial_interface.SerialInterface()

BROADCAST_ADDR = 4294967295

telemetry_data = telemetry_pb2.Telemetry()
telemetry_data.environment_metrics.temperature = 352.222
telemetry_data.environment_metrics.relative_humidity = 69
telemetry_data.environment_metrics.barometric_pressure = 0
telemetry_data.environment_metrics.gas_resistance = 0
telemetry_data.environment_metrics.voltage = 0
telemetry_data.environment_metrics.current = 0

interface.sendData(
    telemetry_data,
    destinationId=BROADCAST_ADDR,
    portNum=portnums_pb2.PortNum.TELEMETRY_APP,
    wantResponse=False,
)

interface.close()