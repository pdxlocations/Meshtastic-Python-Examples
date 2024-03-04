import meshtastic.serial_interface
from meshtastic import mesh_pb2
from pubsub import pub

interface = meshtastic.serial_interface.SerialInterface()

def onReceive(packet, interface):
    # Print all packets
    # print(f"{packet} \n\n") 

    print("Received packet:")
    print(f"  From: {packet['from']}")
    print(f"  To: {packet['to']}")
    
    if 'decoded' in packet:
        print(f"  Port Number: {packet['decoded'].get('portnum', 'N/A')}")
        
        if packet['decoded'].get('portnum') == 'NODEINFO_APP':
            print("  Node Information:")
            node_info = packet['decoded'].get('user', {})
            print(f"    ID: {node_info.get('id', 'N/A')}")
            print(f"    Long Name: {node_info.get('longName', 'N/A')}")
            print(f"    Short Name: {node_info.get('shortName', 'N/A')}")
            print(f"    MAC Address: {node_info.get('macaddr', 'N/A')}")
            print(f"    Hardware Model: {node_info.get('hwModel', 'N/A')}")

        elif packet['decoded'].get('portnum') == 'POSITION_APP':
            print("  Position:")
            position = packet['decoded']['position']
            print(f"    Latitude: {position.get('latitude', 'N/A')}")
            print(f"    Longitude: {position.get('longitude', 'N/A')}")
            print(f"    Altitude: {position.get('altitude', 'N/A')}")

        elif packet['decoded'].get('portnum') == 'TEXT_MESSAGE_APP':
            print("  Text Message:")
            print(f"    Text: {packet['decoded']['text']}")

        elif packet['decoded'].get('portnum') == 'TELEMETRY_APP':
            print("  Telemetry:")
            telemetry = packet['decoded'].get('telemetry', {})
            print(f"    Time: {telemetry.get('time', 'N/A')}")
            print("    Device Metrics:")

            device_metrics = telemetry.get('deviceMetrics', {})
            if device_metrics:
                print(f"      Battery Level: {device_metrics.get('batteryLevel', 'N/A')}")
                print(f"      Voltage: {device_metrics.get('voltage', 'N/A')}")
                print(f"      Channel Utilization: {device_metrics.get('channelUtilization', 'N/A')}")
                print(f"      Air Utilization Tx: {device_metrics.get('airUtilTx', 'N/A')}")

            power_metrics = telemetry.get('powerMetrics', {})
            if power_metrics:
                print("    Power Metrics:")
                print(f"      CH1 Voltage: {power_metrics.get('ch1_voltage', 'N/A')}")
                print(f"      CH1 Current: {power_metrics.get('ch1_current', 'N/A')}")
                print(f"      CH2 Voltage: {power_metrics.get('ch2_voltage', 'N/A')}")
                print(f"      CH2 Current: {power_metrics.get('ch2_current', 'N/A')}")

            environment_metrics = telemetry.get('environmentMetrics', {})
            if environment_metrics:
                print("    Environment Metrics:")
                print(f"      Temperature: {environment_metrics.get('temperature', 'N/A')}")
                print(f"      Relative Humidity: {environment_metrics.get('relativeHumidity', 'N/A')}")
                print(f"      Barometric Pressure: {environment_metrics.get('barometricPressure', 'N/A')}")

        elif packet['decoded'].get('portnum') == 'NEIGHBORINFO_APP':
            # Neighbor Information
            print("  Neighbor Information:")
            message = mesh_pb2.NeighborInfo()
            payload_bytes = packet['decoded'].get('payload', b'')
            message.ParseFromString(payload_bytes)
            print(f"    Node ID: {message.node_id}")
            print(f"    Last Sent By ID: {message.last_sent_by_id}")
            print(f"    Node Broadcast Interval (secs): {message.node_broadcast_interval_secs}")
            print("    Neighbors:")
            for neighbor in message.neighbors:
                print(f"      Neighbor ID: {neighbor.node_id}")
                print(f"        SNR: {neighbor.snr}")

        elif packet['decoded'].get('portnum') == 'RANGE_TEST_APP':
            print("  Range Test Information:")
            payload = packet['decoded'].get('payload', b'')
            print(f"    Payload: {payload.decode()}")
        
        elif packet['decoded'].get('portnum') == 'STORE_FORWARD_APP':
            print("  Store Forward Information:")
            payload = packet['decoded'].get('payload', b'')
            print(f"    Payload: {payload}")

        elif packet['decoded'].get('portnum') == 'ADMIN_APP':
            print("  Administrative Information:")
            payload = packet['decoded'].get('payload', b'')
            print(f"    Payload: {payload}")
            admin_info = packet['decoded'].get('admin', {})
            if 'getChannelResponse' in admin_info:
                response = admin_info['getChannelResponse']
                print("    Get Channel Response:")
                print(f"      Index: {response.get('index', 'N/A')}")
                print("      Settings:")
                settings = response.get('settings', {})
                for key, value in settings.items():
                    print(f"        {key}: {value}")
        
        else:
            print("  No telemetry, position, or text message data in the decoded packet.")
    else:
        print("  No 'decoded' key found in the packet. Our node doesn't have the encryption key!")
        
    print()

pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    pass
