from meshtastic.protobuf import mesh_pb2, channel_pb2, config_pb2, module_config_pb2

def generate_menu_from_protobuf(message_instance):
    if not hasattr(message_instance, "DESCRIPTOR"):
        return None  # Return None for non-protobuf instances
    menu = {}

    field_names = message_instance.DESCRIPTOR.fields_by_name.keys()
    for field_name in field_names:
        field_descriptor = message_instance.DESCRIPTOR.fields_by_name[field_name]
        if field_descriptor is not None:
            value = getattr(message_instance, field_name)
            if value is not None:  # Exclude None values
                if hasattr(value, "DESCRIPTOR"):  # Handle nested protobuf
                    menu[field_name] = generate_menu_from_protobuf(value)
                else:
                    menu[field_name] = str(value) if isinstance(value, bytes) else value  # Convert binary strings
    return menu

# Instantiate protobuf objects
user = mesh_pb2.User()
user_settings = ["long_name", "short_name", "is_licensed","is_unmessagable"]
user_config = generate_menu_from_protobuf(user)
user_config = {key: value if value != "" else "" for key, value in user_config.items() if key in user_settings}

channel = channel_pb2.ChannelSettings()
channel_config = generate_menu_from_protobuf(channel)
channel_config = [{key: (value if value != "" else "") for key, value in channel_config.items()} for _ in range(8)]

radio = config_pb2.Config()
radio_config = generate_menu_from_protobuf(radio)

module = module_config_pb2.ModuleConfig()
module_config = generate_menu_from_protobuf(module)

# Pretty print function for JSON-like output
def pretty_print(title, data, indent=0):
    spacing = " " * indent
    if isinstance(data, dict):
        print(f"{spacing}{title}: {{")
        for i, (key, value) in enumerate(data.items()):
            is_last = i == len(data) - 1
            if isinstance(value, (dict, list)):
                pretty_print(f'"{key}"', value, indent + 2)
            else:
                print(f'{spacing}  "{key}": {repr(value).lower() if isinstance(value, bool) else repr(value)}{"," if not is_last else ""}')
        print(f"{spacing}}}{',' if indent > 0 else ''}")
    elif isinstance(data, list):
        print(f"{spacing}{title}: [")
        for i, item in enumerate(data):
            is_last = i == len(data) - 1
            if isinstance(item, (dict, list)):
                pretty_print("", item, indent + 2)
            else:
                print(f"{spacing}  {repr(item)}{',' if not is_last else ''}")
        print(f"{spacing}]{',' if indent > 0 else ''}")
    else:
        print(f'{spacing}{title}: {repr(data)}')

# Print the final structured data
print("{")
pretty_print('"User Config"', user_config, 2)
pretty_print('"Channel Config"', channel_config, 2)
pretty_print('"Radio Config"', radio_config, 2)
pretty_print('"Module Config"', module_config, 2)
print("}")