import paho.mqtt.client as mqtt
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from meshtastic.protobuf import mqtt_pb2, mesh_pb2
from meshtastic import protocols

BROKER = "mqtt.meshtastic.org"
USER = "meshdev"
PASS = "large4cats"
PORT = 1883
TOPICS = ["msh/US/2/e/LongFast/#","msh/US/2/e/PKI/#"]
KEY = "AQ=="
KEY = "1PG7OiApB1nwvP+rz05pAQ==" if KEY == "AQ==" else KEY

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a message is received
def on_message(client, userdata, msg):
    se = mqtt_pb2.ServiceEnvelope()
    se.ParseFromString(msg.payload)
    decoded_mp = se.packet

    # Decrypt the payload if necessary
    if decoded_mp.HasField("encrypted") and not decoded_mp.HasField("decoded"):
        decoded_data = decrypt_packet(decoded_mp, KEY)
        if decoded_data is None:
            print("Decryption failed; skipping message")
            return
    else:
        decoded_data = decoded_mp.decoded
    decoded_mp.decoded.CopyFrom(decoded_data)

    portNumInt = decoded_mp.decoded.portnum
    handler = protocols.get(portNumInt)
    pb = None
    if handler is not None and handler.protobufFactory is not None:
        pb = handler.protobufFactory()
        pb.ParseFromString(decoded_mp.decoded.payload)

    if pb:
        pb = str(pb).replace('\n', ' ').replace('\r', ' ').strip()
        decoded_mp.decoded.payload = pb.encode("utf-8")

    print(decoded_mp)


def decrypt_packet(mp, key):
    try:
        key_bytes = base64.b64decode(key.encode('ascii'))

        # Build the nonce from message ID and sender
        nonce_packet_id = getattr(mp, "id").to_bytes(8, "little")
        nonce_from_node = getattr(mp, "from").to_bytes(8, "little")
        nonce = nonce_packet_id + nonce_from_node

        # Decrypt the encrypted payload
        cipher = Cipher(algorithms.AES(key_bytes), modes.CTR(nonce), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(getattr(mp, "encrypted")) + decryptor.finalize()

        # Parse the decrypted bytes into a Data object
        data = mesh_pb2.Data()
        data.ParseFromString(decrypted_bytes)
        return data

    except Exception as e:
        print(f"Failed to decrypt: {e}")
        data = mesh_pb2.Data()
        return data

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(USER, PASS)
try:
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_forever()
except Exception as e:
    print(f"An error occurred: {e}")