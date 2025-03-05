import meshtastic.serial_interface
import base64
import logging
import time

logging.basicConfig(level=logging.INFO)

new_keys = [
    'D4Xi3qdGihJj1gTo2T6lyw6fqKudb/3aWncKJAdZikE=', 
    'K7Pm5qGWiKd5K8XpK2+7DwJFlL3aZG5D8F+eC34U5DY=', 
    'zQvX5UuY0V7qMgF2PvAlV+5OMqUQ8DdKkHE7GvVJEBU='
]

# Remove "base64:" prefix and decode
decoded_keys = [base64.b64decode(key) for key in new_keys]

interface = meshtastic.serial_interface.SerialInterface()
ourNode = interface.getNode('^local')

# Get reference to security config
security_config = ourNode.localConfig.security

# Clear existing keys if needed
if len(security_config.admin_key) > 0:
    logging.info("Clearing existing admin keys...")
    del security_config.admin_key[:]
    ourNode.writeConfig("security")
    time.sleep(1)  # Give time for device to process

# Append new keys
for key in decoded_keys:
    logging.info(f"Adding admin key: {key}")
    security_config.admin_key.append(key)

ourNode.writeConfig("security")

logging.info("Admin keys updated successfully!")