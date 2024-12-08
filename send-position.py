import meshtastic.serial_interface
from meshtastic import BROADCAST_NUM

interface = meshtastic.serial_interface.SerialInterface()

interface.sendPosition(
    latitude = 45,
    longitude = -120,
    altitude = 100,
    destinationId = BROADCAST_NUM,
    wantAck = False,
    wantResponse = False,
)

interface.close()