import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 40700)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address);

# XM02Xza

try:
    
    # Send data
    message =  '<?xml version="1.0" encoding="utf-8"?>' + \
    '<ClientIntegrationRequest>' + \
    '<Function>GetPatientRecord</Function>' + \
    '<APIKey>0c6bee20cc99f13b</APIKey>' + \
    '<RequestUID>REQUEST_ID</RequestUID>' + \
    '<DeviceID>a824b6abdab4c355</DeviceID>' + \
    '<DeviceVersion>1.0</DeviceVersion>' + \
    '<FunctionVersion>1.0</FunctionVersion>' + \
    '<FunctionParameters> <Identity> <NhsNumber>4917111072</NhsNumber> </Identity> <LeaveRecordOpen></LeaveRecordOpen> <Filter> <ClinicalCode>X3003</ClinicalCode> <ClinicalCode>XaBVJ</ClinicalCode> <Numeric>XE2mq</Numeric> </Filter> <Medication></Medication> </FunctionParameters>' + \
    '</ClientIntegrationRequest>'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message.encode('utf-8'))

    sock.settimeout(20);
    time.sleep(2)
    data = sock.recv(10025)
    print data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()