import meshtastic.serial_interface
from meshtastic import BROADCAST_NUM
import time

interface = meshtastic.serial_interface.SerialInterface()

current_time = int(time.time())

interface.sendPosition(
    latitude = 45,
    longitude = -120,
    altitude = 100,
    timeSec = current_time,
    destinationId = BROADCAST_NUM,
    wantAck = False,
    wantResponse = False,
)

interface.close()