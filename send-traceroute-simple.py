import meshtastic.serial_interface
interface = meshtastic.serial_interface.SerialInterface()
dest = 1623194643
hopLimit = 3
channelIndex = 0

interface.sendTraceRoute(dest, hopLimit, channelIndex=channelIndex)