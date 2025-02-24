import asyncio
import io
import contextlib
import socket
from pubsub import pub
import meshtastic.tcp_interface

host = '192.168.86.45'

# Function to get firmware version
def getNodeFirmware(interface):
    try:
        output_capture = io.StringIO()
        with contextlib.redirect_stdout(output_capture), contextlib.redirect_stderr(output_capture):
            interface.localNode.getMetadata()

        console_output = output_capture.getvalue()

        if "firmware_version" in console_output:
            return console_output.split("firmware_version: ")[1].split("\n")[0]

        return -1
    except (socket.error, BrokenPipeError, ConnectionResetError, Exception) as e:
        print(f"Error retrieving firmware: {e}")
        raise e  # Propagate the error to handle reconnection

# Async function to retry connection
async def retry_interface():
    print("Retrying connection to the interface...")
    await asyncio.sleep(3)  # Wait before retrying

    try:
        interface = meshtastic.tcp_interface.TCPInterface(hostname=host)
        print("Interface reinitialized successfully.")
        return interface
    except (ConnectionRefusedError, socket.error, Exception) as e:
        print(f"Failed to reinitialize interface: {e}")
        return None

# Function to check connection and reconnect if needed
async def check_and_reconnect(interface):
    if interface is None:
        print("No valid interface. Attempting to reconnect...")
        interface = await retry_interface()
        return interface

    try:
        print("Checking interface connection...")
        fw_ver = getNodeFirmware(interface)
        if fw_ver != -1:
            print(f"Firmware Version: {fw_ver}")
            return interface
        else:
            raise Exception("Failed to retrieve firmware version.")

    except (socket.error, BrokenPipeError, ConnectionResetError, Exception) as e:
        print(f"Error with the interface, setting to None and attempting reconnect: {e}")
        return await retry_interface()

# Main watchdog loop
async def watchdog(interface):
    while True:
        await asyncio.sleep(20)
        interface = await check_and_reconnect(interface)
        if interface:
            print("Interface is connected.")
        else:
            print("Interface connection failed. Retrying...")

# Handle received messages
def onReceive(packet, interface):
    if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
        print(packet)

# Main function
async def main():
    try:
        interface = meshtastic.tcp_interface.TCPInterface(hostname=host)
        print("Interface initialized.")
    except (ConnectionRefusedError, socket.error) as e:
        print(f"Failed to initialize interface: {e}")
        interface = None

    pub.subscribe(onReceive, 'meshtastic.receive')
    await watchdog(interface)

# Run the program
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")