#!/usr/bin/python3
import sys
import readinifile as readini
import getxml as getxml


def getNVRStatus():
	if (sys.argv[2] == 'deviceType') or (sys.argv[2] == 'model') or (sys.argv[2] == 'firmwareVersion') or (	sys.argv[2] == 'deviceName'):
		root = getxml.get_xmltext_fromdevice(sys.argv[1], readini.getsettings('namespace', 'deviceInfo'))
	else:
		root = getxml.get_xmltext_fromdevice(sys.argv[1], readini.getsettings('namespace', 'deviceStatus'))

	try:
		print(root.find('.//{http://www.isapi.org/ver20/XMLSchema}' + sys.argv[2]).text.strip())
	except AttributeError:
		print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + sys.argv[2]).text.strip())

getNVRStatus()
