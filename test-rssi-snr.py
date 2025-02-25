
import meshtastic.serial_interface, meshtastic.tcp_interface
from meshtastic.protobuf import telemetry_pb2, portnums_pb2
from pubsub import pub
import time


# dest = 147281321 ## DUMMY RAK
dest = 963936390 ## MESHSTICK

want_response = True
channel = 0

interface = meshtastic.serial_interface.SerialInterface()
interface = meshtastic.tcp_interface.TCPInterface(hostname="192.168.86.39")

telemetry_data = telemetry_pb2.Telemetry()
telemetry_data.device_metrics.battery_level = 69

response_received = False
last_request_time = None

def signalReport():
    global last_request_time
    global response_received
    # print("Requesting data...")
    response_received = False
    last_request_time = time.time()  # Update last request time
    interface.sendData(
        telemetry_data,
        destinationId=dest,
        portNum=portnums_pb2.PortNum.TELEMETRY_APP,
        wantResponse=want_response
    )

def onReceive(packet, interface):
    global response_received
    if packet['from'] == dest:
        print(f"SNR: {packet['rxSnr']} RSSI: {packet['rxRssi']}")
        response_received = True

pub.subscribe(onReceive, 'meshtastic.receive')

signalReport()  # Initial request

try:
    while True:
        time.sleep(0.1)  # Short sleep to allow quick response check
        if response_received:
            signalReport()  # Send another request after receiving a response
        elif time.time() - last_request_time > 15:
            print("No response received for 10 seconds, retrying...")
            signalReport()  # Retry if no response received for 10 seconds
except KeyboardInterrupt:
    print("Exiting program...")
finally:
    interface.close()
    print("Interface closed. Goodbye!")
