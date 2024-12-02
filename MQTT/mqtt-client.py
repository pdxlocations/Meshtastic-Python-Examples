#!/usr/bin/env python3
"""
Powered by Meshtastic™ https://meshtastic.org/
"""

from meshtastic.protobuf import mesh_pb2, mqtt_pb2, portnums_pb2
from meshtastic import BROADCAST_NUM, protocols
import paho.mqtt.client as mqtt
import random
import time
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import re

#### Debug Options
debug = True
auto_reconnect = True
auto_reconnect_delay = 1 # seconds
print_service_envelope = False
print_message_packet = False

print_node_info =  True
print_node_position = True
print_node_telemetry = True

### Default settings
mqtt_broker = "mqtt.meshtastic.org"
mqtt_port = 1883
mqtt_username = "meshdev"
mqtt_password = "large4cats"
# root_topic = "msh/US/2/e/"
root_topic = "msh/US/Bots/2/e/"
channel = "LongFast"
key = "AQ=="
message_text = "Person man, person man Hit on the head with a frying pan Lives his life in a garbage can"

# Generate 4 random hexadecimal characters to create a unique node name
random_hex_chars = ''.join(random.choices('0123456789abcdef', k=4))
node_name = '!abcd' + random_hex_chars
node_number = int(node_name.replace("!", ""), 16)
global_message_id = random.getrandbits(32)
client_short_name = "BOT"
client_long_name = "Bottastic"
lat = "0"
lon = "0"
alt = "0"
client_hw_model = 255

#################################
### Program variables

default_key = "1PG7OiApB1nwvP+rz05pAQ==" # AKA AQ==

#################################
# Program Base Functions
    
def set_topic():
    if debug: print("set_topic")
    global subscribe_topic, publish_topic
    node_name = '!' + hex(node_number)[2:]
    subscribe_topic = root_topic + channel + "/#"
    publish_topic = root_topic + channel + "/" + node_name

def xor_hash(data):
    result = 0
    for char in data:
        result ^= char
    return result

def generate_hash(name, key):
    replaced_key = key.replace('-', '+').replace('_', '/')
    key_bytes = base64.b64decode(replaced_key.encode('utf-8'))
    h_name = xor_hash(bytes(name, 'utf-8'))
    h_key = xor_hash(key_bytes)
    result = h_name ^ h_key
    return result


#################################
# Receive Messages

def on_message(client, userdata, msg):
    se = mqtt_pb2.ServiceEnvelope()
    try:
        se.ParseFromString(msg.payload)
        if print_service_envelope:
            print ("")
            print ("Service Envelope:")
            print (se)
        mp = se.packet
        if print_message_packet: 
            print ("")
            print ("Message Packet:")
            print(mp)
    except Exception as e:
        print(f"*** ServiceEnvelope: {str(e)}")
        return
    
    if mp.HasField("encrypted") and not mp.HasField("decoded"):
        decode_encrypted(mp)

    # Attempt to process the decrypted or encrypted payload
    portNumInt = mp.decoded.portnum if mp.HasField("decoded") else None
    handler = protocols.get(portNumInt) if portNumInt else None

    pb = None
    if handler is not None and handler.protobufFactory is not None:
        pb = handler.protobufFactory()
        pb.ParseFromString(mp.decoded.payload)

    if pb:
        # Clean and update the payload
        pb_str = str(pb).replace('\n', ' ').replace('\r', ' ').strip()
        mp.decoded.payload = pb_str.encode("utf-8")
    print(mp)


def decode_encrypted(mp):
        try:
            key_bytes = base64.b64decode(key.encode('ascii'))
            nonce_packet_id = getattr(mp, "id").to_bytes(8, "little")
            nonce_from_node = getattr(mp, "from").to_bytes(8, "little")
            nonce = nonce_packet_id + nonce_from_node
            cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_bytes = decryptor.update(getattr(mp, "encrypted")) + decryptor.finalize()
            data = mesh_pb2.Data()
            data.ParseFromString(decrypted_bytes)
            mp.decoded.CopyFrom(data)
        except Exception as e:
            if print_message_packet: print(f"failed to decrypt: \n{mp}")
            if debug: print(f"*** Decryption failed: {str(e)}")
            return

#################################
# Send Messages

def direct_message(destination_id):
    if debug: print("direct_message")
    if destination_id:
        try:
            destination_id = int(destination_id[1:], 16)
            send_message(destination_id)
        except Exception as e:
            if debug: print(f"Error converting destination_id: {e}")

def send_message(destination_id, message_text):
    if not client.is_connected():
        connect_mqtt()

    if message_text:
        encoded_message = mesh_pb2.Data()
        encoded_message.portnum = portnums_pb2.TEXT_MESSAGE_APP 
        encoded_message.payload = message_text.encode("utf-8")
        generate_mesh_packet(destination_id, encoded_message)
    else:
        return

def send_traceroute(destination_id):
    if not client.is_connected():
        connect_mqtt()
    if debug: print(f"Sending Traceroute Packet to {str(destination_id)}")

    encoded_message = mesh_pb2.Data()
    encoded_message.portnum = portnums_pb2.TRACEROUTE_APP
    encoded_message.want_response = True

    destination_id = int(destination_id[1:], 16)
    generate_mesh_packet(destination_id, encoded_message)

def send_node_info(destination_id, want_response):
    if client.is_connected():
        user_payload = mesh_pb2.User()
        setattr(user_payload, "id", node_name)
        setattr(user_payload, "long_name", client_long_name)
        setattr(user_payload, "short_name", client_short_name)
        setattr(user_payload, "hw_model", client_hw_model)

        user_payload = user_payload.SerializeToString()

        encoded_message = mesh_pb2.Data()
        encoded_message.portnum = portnums_pb2.NODEINFO_APP
        encoded_message.payload = user_payload
        encoded_message.want_response = want_response  # Request NodeInfo back
        generate_mesh_packet(destination_id, encoded_message)

def send_position(destination_id):
    if client.is_connected():
        pos_time = int(time.time())
        latitude = int(float(lat) * 1e7)
        longitude = int(float(lon) * 1e7)
        altitude_units = 1 / 3.28084 if 'ft' in str(alt) else 1.0
        altitude = int(altitude_units * float(re.sub('[^0-9.]', '', str(alt))))

        position_payload = mesh_pb2.Position()
        setattr(position_payload, "latitude_i", latitude)
        setattr(position_payload, "longitude_i", longitude)
        setattr(position_payload, "altitude", altitude)
        setattr(position_payload, "time", pos_time)

        position_payload = position_payload.SerializeToString()

        encoded_message = mesh_pb2.Data()
        encoded_message.portnum = portnums_pb2.POSITION_APP
        encoded_message.payload = position_payload
        encoded_message.want_response = True

        generate_mesh_packet(destination_id, encoded_message)

def generate_mesh_packet(destination_id, encoded_message):
    global global_message_id
    mesh_packet = mesh_pb2.MeshPacket()

    # Use the global message ID and increment it for the next call
    mesh_packet.id = global_message_id
    global_message_id += 1
    
    setattr(mesh_packet, "from", node_number)
    mesh_packet.to = destination_id
    mesh_packet.want_ack = False
    mesh_packet.channel = generate_hash(channel, key)
    mesh_packet.hop_limit = 3

    if key == "":
        mesh_packet.decoded.CopyFrom(encoded_message)
    else:
        mesh_packet.encrypted = encrypt_message(channel, key, mesh_packet, encoded_message)

    service_envelope = mqtt_pb2.ServiceEnvelope()
    service_envelope.packet.CopyFrom(mesh_packet)
    service_envelope.channel_id = channel
    service_envelope.gateway_id = node_name

    payload = service_envelope.SerializeToString()
    client.publish(publish_topic, payload)

def encrypt_message(channel, key, mesh_packet, encoded_message):
    mesh_packet.channel = generate_hash(channel, key)
    key_bytes = base64.b64decode(key.encode('ascii'))
    nonce_packet_id = mesh_packet.id.to_bytes(8, "little")
    nonce_from_node = node_number.to_bytes(8, "little")
    nonce = nonce_packet_id + nonce_from_node
    cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(encoded_message.SerializeToString()) + encryptor.finalize()
    return encrypted_bytes

def send_ack(destination_id, message_id):
    if debug: print("Sending ACK")
    encoded_message = mesh_pb2.Data()
    encoded_message.portnum = portnums_pb2.ROUTING_APP
    encoded_message.request_id = message_id
    encoded_message.payload = b"\030\000"
    generate_mesh_packet(destination_id, encoded_message)


#################################
# MQTT Server 
    
def connect_mqtt():
    if "tls_configured" not in connect_mqtt.__dict__:          #Persistent variable to remember if we've configured TLS yet
        connect_mqtt.tls_configured = False

    if debug: print("connect_mqtt")
    global mqtt_broker, mqtt_port, mqtt_username, mqtt_password, root_topic, channel, node_number, db_file_path, key
    if not client.is_connected():
        try:
            if ':' in mqtt_broker:
                mqtt_broker,mqtt_port = mqtt_broker.split(':')
                mqtt_port = int(mqtt_port)

            if key == "AQ==":
                if debug: print("key is default, expanding to AES128")
                key = "1PG7OiApB1nwvP+rz05pAQ=="

            padded_key = key.ljust(len(key) + ((4 - (len(key) % 4)) % 4), '=')
            replaced_key = padded_key.replace('-', '+').replace('_', '/')
            key = replaced_key

            client.username_pw_set(mqtt_username, mqtt_password)
            if mqtt_port == 8883 and connect_mqtt.tls_configured == False:
                client.tls_set(ca_certs="cacert.pem", tls_version=ssl.PROTOCOL_TLSv1_2)
                client.tls_insecure_set(False)
                connect_mqtt.tls_configured = True
            client.connect(mqtt_broker, mqtt_port, 60)
            client.loop_start()

        except Exception as e:
            print (e)

def disconnect_mqtt():
    if debug: print("disconnect_mqtt")
    if client.is_connected():
        client.disconnect()

def on_connect(client, userdata, flags, reason_code, properties):
    set_topic()
    if client.is_connected():
        print("client is connected")
    
    if reason_code == 0:
        if debug: print(f"Connected to sever: {mqtt_broker}")
        if debug: print(f"Subscribe Topic is: {subscribe_topic}")
        if debug: print(f"Publish Topic is: {publish_topic}\n")
        client.subscribe(subscribe_topic)

def on_disconnect(client, userdata, flags, reason_code, properties):
    if debug: print("on_disconnect")
    if reason_code != 0:
        if auto_reconnect == True:
            print("attempting to reconnect in " + str(auto_reconnect_delay) + " second(s)")
            time.sleep(auto_reconnect_delay)
            connect_mqtt()

############################
# Main 

def main():
    global client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="", clean_session=True, userdata=None)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    connect_mqtt()
    time.sleep(1)

    if client.is_connected:
        send_node_info(BROADCAST_NUM, want_response=False)
        time.sleep(4)
        send_position(BROADCAST_NUM)
        time.sleep(4)
        send_message(BROADCAST_NUM, message_text)
        time.sleep(4)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()