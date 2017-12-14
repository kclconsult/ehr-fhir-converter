import socket
import sys
import time
import xml.dom.minidom

PORT_O   = 40698
PORT_N   = 40700
HOSTNAME = 'localhost'
MSG_SIZE = 1024

xml_f = open(sys.argv[1])
req = xml_f.readlines()
req_s = ''.join(line.strip() for line in req)
res = ''

s = socket.socket()
s.settimeout(1.0)
s.connect((HOSTNAME, PORT_N))
s.send(req_s + '\n')

while True:
   #time.sleep(1)
    try:
        data = s.recv(MSG_SIZE)
	print data
    	if not data:
	    break
    	else:
            res += data
	    if res[-1] == '\n':
		print 'EOF'
	        break
    except socket.error as e:
	print 'socket error: %s' % e
	break

s.close()

print res
xml = xml.dom.minidom.parseString(res)
print xml.toprettyxml()
