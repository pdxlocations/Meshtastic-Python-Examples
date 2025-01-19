import meshtastic.serial_interface
from meshtastic.protobuf import channel_pb2
import base64

interface = meshtastic.serial_interface.SerialInterface()
node = interface.getNode('^local')

edit_channel = 1
new_settings = {'psk': 'AQ==', 'name': 'NBC', 'uplink_enabled': True, 'downlink_enabled': True, 'position_precision': 13}

channel = node.channels[edit_channel]

for key, value in new_settings.items():
    if key == 'psk':  # Special case: decode Base64 for psk
        channel.settings.psk = base64.b64decode(value)
    elif key == 'position_precision':  # Special case: module_settings
        channel.settings.module_settings.position_precision = value
    else:
        setattr(channel.settings, key, value)  # Use setattr for other fields

if edit_channel == 0:
    channel.role = channel_pb2.Channel.Role.PRIMARY
else:
    channel.role = channel_pb2.Channel.Role.SECONDARY

node.writeChannel(edit_channel)
print(node.channels)

interface.close()