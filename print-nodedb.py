import meshtastic.serial_interface
iface = meshtastic.serial_interface.SerialInterface()
if iface.nodes:
    for node in iface.nodes.values():
        # print (node)

        print("Node ID:", node["user"]["id"])
        print("Long Name:", node["user"]["longName"])
        print("Short Name:", node["user"]["shortName"])
        print("MAC Address:", node["user"]["macaddr"])
        print("Hardware Model:", node["user"]["hwModel"])

        if "snr" in node:
            print("SNR:", node["snr"])
        if "lastHeard" in node:
            print("Last Heard:", node["lastHeard"])
        if "hopsAway" in node:
            print("Hops Away:", node["hopsAway"])

        if "position" in node:
            if "latitude" in node["position"]:
                print("Latitude:", node["position"]["latitude"])
            if "longitude" in node["position"]:
                print("Longitude:", node["position"]["longitude"])
            if "altitude" in node["position"]:
                print("Altitude:", node["position"]["altitude"])
            if "time" in node["position"]:
                print("Time:", node["position"]["time"])

        if "deviceMetrics" in node:
            if "batteryLevel" in node["deviceMetrics"]:
                print("Battery Level:", node["deviceMetrics"]["batteryLevel"])
            if "voltage" in node["deviceMetrics"]:
                print("Voltage:", node["deviceMetrics"]["voltage"])
            if "channelUtilization" in node["deviceMetrics"]:
                print("Channel Utilization:", node["deviceMetrics"]["channelUtilization"])
            if "airUtilTx" in node["deviceMetrics"]:
                print("Air Util Tx:", node["deviceMetrics"]["airUtilTx"])

        print("\n")
iface.close()
