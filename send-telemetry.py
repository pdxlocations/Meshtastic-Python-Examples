import meshtastic.serial_interface
from meshtastic import BROADCAST_NUM

telemetry_type = "device_metrics" # environment_metrics, air_quality_metrics, power_metrics, local_stats
want_response = False
channel = 0

interface = meshtastic.serial_interface.SerialInterface()
interface.sendTelemetry(BROADCAST_NUM, want_response, channel, telemetry_type)
interface.close()