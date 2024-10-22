import meshtastic.serial_interface
from pubsub import pub
import time

interface = meshtastic.serial_interface.SerialInterface()

def onReceive(packet, interface):
    if 'decoded' in packet and packet['decoded']['portnum'] == 'TRACEROUTE_APP':

        routeBack = packet['decoded']['traceroute']['routeBack']
        route = packet['decoded']['traceroute']['route']

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
