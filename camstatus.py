#!/usr/bin/python3

"""Получение сведений о камере подключенной к регистратору
# ПЕРЕДАВАЕМЫЕ ПАРАМЕТРЫ
1-Имя регистратора (как указано в файле settings.ini)
2-Тэг значение которого мы ищем
3-ID камеры на регистраторе
"""

import sys
import readinifile as readini
import getxml as getxml

deviceName = sys.argv[1]
deviceParameter = sys.argv[2]
channel_ID = sys.argv[3]


def getCAMStatus():
    if (deviceParameter == 'online') or (deviceParameter == 'ipAddress') or (deviceParameter == 'chanDetectResult'):
        root = getxml.get_xmltext_fromdevice(deviceName,
                                         readini.getsettings('namespace', 'channels') + channel_ID + '/status')
        try:
            return root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + deviceParameter).text.strip()
            # print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + deviceParameter).text.strip())
        except AttributeError:
            # print(root.find('.//{urn:ISAPIlliance-org}' + deviceParameter).text.strip())
            return root.find('.//{urn:ISAPIlliance-org}' + deviceParameter).text.strip()

    elif deviceParameter == 'deviceName':
        root = getxml.get_xmltext_fromdevice(deviceName, readini.getsettings('namespace', 'channels') + channel_ID)
        try:
            # print(root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + 'name').text.strip())
            return root.find('.//{http://www.hikvision.com/ver20/XMLSchema}' + 'name').text.strip()
        except AttributeError:
            # print(root.find('.//{urn:ISAPIlliance-org}' + 'name').text.strip())
            return root.find('.//{urn:ISAPIlliance-org}' + 'name').text.strip()


try:
    hikdata = getCAMStatus()
    print(hikdata)
except:
    print("NotSupported")

# todo
# http://192.168.2.1/ISAPI/ContentMgmt/InputProxy/channels/1/video/motionDetection
