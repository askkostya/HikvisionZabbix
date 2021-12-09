#!/usr/bin/python3

import sys
import readinifile as readini
import getxml as getxml

deviceName = sys.argv[1]
deviceParameter = sys.argv[2]
channel_ID = sys.argv[3]

root = getxml.get_xmltext_fromdevice(deviceName, readini.getsettings('namespace', 'hddStatus') + channel_ID)
if root == 'No route to host':
	print(root)
else:
	try:
		print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + deviceParameter).text.strip())
	except AttributeError:
		print(root.find('.//{urn:ISAPIlliance-org}' + deviceParameter).text.strip())
