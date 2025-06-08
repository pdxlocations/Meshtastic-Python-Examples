import meshtastic.serial_interface
import time

interface = meshtastic.serial_interface.SerialInterface()

url1 = 'https://meshtastic.org/e/#CgcSAQE6AggNEgwIATgBQANIAVAeaAE'
url2 = 'https://meshtastic.org/e/#ChISAQUaCWNoYW5uZWwwMToCCA0SDAgBOAFAA0gBUB5oAQ'

old_url = interface.localNode.getURL()
print (old_url)

interface.localNode.setURL(url1)

time.sleep(4)
new_url = interface.localNode.getURL()
print (new_url)
