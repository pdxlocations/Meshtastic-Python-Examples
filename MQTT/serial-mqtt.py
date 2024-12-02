import meshtastic.serial_interface
import paho.mqtt.client as mqtt
from pubsub import pub
import json
import time

# Configure MQTT broker
mqtt_broker = 'mqtt.meshtastic.org'
mqtt_port = 1883
mqtt_user = "meshdev"
mqtt_pass = "large4cats"
mqtt_topic = "msh/sMQTT/2/json/LongFast/"
virtual_node = "!deadbeef"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")

def onReceive(packet, interface):
    if 'decoded' not in packet:
        return
    
    data = {
        'channel': 0,
        'from': packet.get('from', ''),
        'hop_start': None,
        'hops_away': None,
        'id': packet.get('id', ''),
        'payload': {},
        'rssi': packet.get('rxRssi', None),
        'sender': virtual_node,
        'snr': packet.get('snr', None),
        'timestamp': packet.get('rxTime', None),
        'to': packet.get('to', None),
        'type': ''
    }

    portnum = packet['decoded'].get('portnum')
    payload = data['payload']

    if portnum == 'NODEINFO_APP':
        data['type'] = 'nodeinfo'
        user = packet['decoded']['user']
        payload.update({
            'hardware': user['hwModel'],
            'id': user['id'],
            'longname': user['longName'],
            'shortname': user['shortName']
        })

    elif portnum == 'POSITION_APP':
        data['type'] = 'position'
        position = packet['decoded']['position']
        payload.update({
            'PDOP': position.get('pdop'),
            'altitude': position.get('altitude'),
            'groundSpeed': position.get('ground_speed'),
            'latitude_i': position['latitudeI'],
            'longitude_i': position['longitudeI'],
            'precision_bits': position.get('precisionBits'),
            'satsInView': position.get('sats_in_view'),
            'time': position.get('time')
        })

    elif portnum == 'TEXT_MESSAGE_APP':
        data['type'] = 'textMessage'
        payload['text'] = packet['decoded']['text']

    elif portnum == 'TELEMETRY_APP':
        data['type'] = 'telemetry'
        telemetry = packet['decoded']['telemetry']
        
        if 'deviceMetrics' in telemetry:
            device_metrics = telemetry['deviceMetrics']
            payload.update({
                'air_util_tx': device_metrics.get('airUtilTx'),
                'battery_level': device_metrics.get('batteryLevel'),
                'channel_utilization': device_metrics.get('channelUtilization'),
                'uptime_seconds': device_metrics.get('uptimeSeconds'),
                'voltage': device_metrics.get('voltage')
            })

        if 'powerMetrics' in telemetry:
            power_metrics = telemetry['powerMetrics']
            payload.update({
                'current_ch1': power_metrics.get('ch1Current'),
                'current_ch2': power_metrics.get('ch2Current'),
                'current_ch3': power_metrics.get('ch3Current'),
                'voltage_ch1': power_metrics.get('ch1Voltage'),
                'voltage_ch2': power_metrics.get('ch2Voltage'),
                'voltage_ch3': power_metrics.get('ch3Voltage')
            })

        if 'environmentMetrics' in telemetry:
            environment_metrics = telemetry['environmentMetrics']
            payload.update({
                'barometric_pressure': environment_metrics.get('barometricPressure'),
                'current': environment_metrics.get('current'),
                'gas_resistance': environment_metrics.get('gasResistance'),
                'iaq': environment_metrics.get('iaq'),
                'lux': environment_metrics.get('lux'),
                'temperature': environment_metrics.get('temperature'),
                'voltage': environment_metrics.get('voltage'),
                'white_lux': environment_metrics.get('whiteLux'),
                'wind_direction': environment_metrics.get('windDirection'),
                'wind_speed': environment_metrics.get('windSpeed')
            })
    else:
        data['type'] = 'todo'
    
    # TODO
    # REMOTE_HARDWARE_APP
    # ROUTING_APP
    # ADMIN_APP
    # TEXT_MESSAGE_COMPRESSED_APP
    # WAYPOINT_APP
    # AUDIO_APP
    # DETECTION_SENSOR_APP
    # REPLY_APP
    # IP_TUNNEL_APP
    # PAXCOUNTER_APP
    # SERIAL_APP
    # STORE_FORWARD_APP
    # RANGE_TEST_APP
    # TRACEROUT_APP
    # NEIGHBORINFO_APP
    # ATAK_PLUGIN
    # MAP_REPORT_APP
    # POWERSTRESS_APP
    # PRIVATE_APP
    # ATAK_FORWARDER

    # Remove keys with None values
    data = {key: value for key, value in data.items() if value is not None}
    payload = {key: value for key, value in payload.items() if value not in (None, '')}
    data['payload'] = payload

    json_data = json.dumps(data, indent=2)
    print(json_data)


        # if 'decoded' in packet:
        # print (packet)
    print ("")


    # Publish the message to the MQTT broker
    client.publish(mqtt_topic + virtual_node, json_data)


# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="", clean_session=True, userdata=None)
client.username_pw_set(mqtt_user, mqtt_pass)
client.connect(mqtt_broker, mqtt_port, 60)
# client.on_disconnect = on_disconnect
# client.on_message = on_message
client.loop_start()
client.on_connect = on_connect

# Initialize serial connection
interface = meshtastic.serial_interface.SerialInterface()
pub.subscribe(onReceive, 'meshtastic.receive')

while True:
    time.sleep(1)
