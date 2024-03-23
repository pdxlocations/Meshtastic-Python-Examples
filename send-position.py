import meshtastic.serial_interface
import time

interface = meshtastic.serial_interface.SerialInterface()

BROADCAST_ADDR = 4294967295
current_time = int(time.time())

interface.sendPosition(
    latitude = 45,
    longitude = -120,
    altitude = 100,
    timeSec = current_time,
    destinationId = BROADCAST_ADDR,
    wantAck = False,
    wantResponse = False,
)

interface.close()