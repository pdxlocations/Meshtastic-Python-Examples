from meshtastic.protobuf import telemetry_pb2

data= b"\r\232+Dg\032\n\r\341z \301\025\000\200\241B"
telem = telemetry_pb2.Telemetry()
telem.ParseFromString(data)

print (telem)