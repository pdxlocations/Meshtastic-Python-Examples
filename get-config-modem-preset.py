import meshtastic.serial_interface
from meshtastic.protobuf import config_pb2

interface = meshtastic.serial_interface.SerialInterface()

ourNode = interface.getNode('^local')

# Get the enum value of modem_preset
modem_preset_enum = ourNode.localConfig.lora.modem_preset

# Get the string representation of the enum value
modem_preset_string = config_pb2.Config.LoRaConfig.ModemPreset.Name(modem_preset_enum)

print(modem_preset_string)