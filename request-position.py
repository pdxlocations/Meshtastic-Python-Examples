
import meshtastic.serial_interface
from meshtastic import BROADCAST_NUM

interface = meshtastic.serial_interface.SerialInterface()
dest = 1623194643

interface.sendPosition(
    destinationId = dest,
    wantResponse = True,
)
