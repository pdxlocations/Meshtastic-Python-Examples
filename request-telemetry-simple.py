import meshtastic.serial_interface

remote_node = 1623194643
want_response = True
channel = 0

interface = meshtastic.serial_interface.SerialInterface()
interface.sendTelemetry(remote_node, want_response, channel)
interface.close()