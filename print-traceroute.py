
from pubsub import pub
import time
import meshtastic.serial_interface, meshtastic.tcp_interface
interface = meshtastic.serial_interface.SerialInterface()
# interface = meshtastic.tcp_interface.TCPInterface(hostname="192.168.86.39")

dest = 1623194643
hopLimit = 5
channelIndex = 0

interface.sendTraceRoute(dest, hopLimit, channelIndex=channelIndex)

def onReceive(packet, interface):
    if 'decoded' in packet and packet['decoded']['portnum'] == 'TRACEROUTE_APP':

        routeBack = packet['decoded']['traceroute'].get('routeBack', [])
        route = packet['decoded']['traceroute'].get('route', [])

        message = f"{packet['to']}"

        if routeBack:
            message += f" --> {' --> '.join(map(str, routeBack))}"

        message += f" --> {packet['from']}"

        if route:
            message += f" --> {' --> '.join(map(str, route))}"

        message += f" --> {packet['to']}"

        print(message)

pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    time.sleep(1)