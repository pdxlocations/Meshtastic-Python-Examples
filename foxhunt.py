import meshtastic.serial_interface
from meshtastic.protobuf import telemetry_pb2, portnums_pb2
from pubsub import pub
import time

remote_node = 182032979
want_response = True
channel = 0
run = True

interface = meshtastic.serial_interface.SerialInterface()

telemetry_data = telemetry_pb2.Telemetry()
telemetry_data.device_metrics.battery_level = 69

def signalReport():
    interface.sendData(
        telemetry_data,
        destinationId=remote_node,
        portNum=portnums_pb2.PortNum.TELEMETRY_APP,
        wantResponse=want_response
    )

def onReceive(packet, interface):
    global run
    if packet['from'] == remote_node: 
        print(f"\nSNR: {packet['rxSnr']} RSSI: {packet['rxRssi']} \n\n")
        # print(f"{packet} \n\n")
        run = False

pub.subscribe(onReceive, 'meshtastic.receive')

signalReport()

while run:
    time.sleep(1)

interface.close()