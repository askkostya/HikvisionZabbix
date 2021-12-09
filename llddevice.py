#!/usr/bin/python3
# coding=utf-8

"""Low level discovery script для обнаружения камер и накопителей в видеорегистраторах
ПЕРЕДАВАЕМЫЙ ПАРАМЕТР
CAM - камеры подключенные к устройствам
HDD - накопители подключенные к устройствам
NVR - Регистраторы
"""

import re
import requests
import sys
import readinifile as readini
from xml.etree import cElementTree as ET


deviceType = sys.argv[1]
if deviceType == 'HDD':
    towwwpage = '/ISAPI/ContentMgmt/Storage/hdd'
    rootxmltree = 'hdd'
    devicename = 'id'
if deviceType == 'CAM':
    towwwpage = '/ISAPI/ContentMgmt/InputProxy/channels/'
    rootxmltree = 'InputProxyChannel'
    devicename = 'name'
# ToDo (исправить)
if deviceType == 'NVR':
    towwwpage = '/ISAPI/ContentMgmt/Storage/hdd'
    rootxmltree = 'hdd'
    devicename = 'id'

deviceList = readini.getAllNVRdevice()
jsondeviceid = ''


def returnRootDeviceList(deviceList):
    r = requests.get('http://' + readini.getip(deviceList[i]) + towwwpage,
                     auth=(readini.getlogin(deviceList[i]), readini.getpassword(deviceList[i])), stream=True)
    xmlstring = re.sub('\\sxmlns="[^"]+"', '', r.text, count=40)
    return ET.fromstring(xmlstring)


def returnJSONData(deviceType, device_id, deviceList):
    if deviceType == 'HDD':
        jsondevicefind = ('{"{#DEVICEID}":"' + device_id + '","{#NVRID}":"' + deviceList[i] + '"')
    elif deviceType == 'CAM':
        jsondevicefind = ('{"{#DEVICENAME}":"' + device_name + '","{#DEVICEID}":"' + device_id + '","{#NVRID}":"' +
                          deviceList[i] + '"')
    return jsondevicefind + '},'


for i in range(len(deviceList)):
    root = returnRootDeviceList(deviceList)

    if deviceType == 'NVR':
        jsondevicefind = ('{"{#NVRID}":"' + deviceList[i] + '"')
        jsondeviceid = jsondevicefind + '},' + jsondeviceid
        continue

    for deviceid in root.findall(rootxmltree):
        device_name = deviceid.find(devicename).text
        device_id = deviceid.find('id').text
        if deviceType == 'HDD':
            jsondevicefind = ('{"{#DEVICEID}":"' + device_id + '","{#NVRID}":"' + deviceList[i] + '"')
        elif deviceType == 'CAM':
            jsondevicefind = ('{"{#DEVICENAME}":"' + device_name + '","{#DEVICEID}":"' + device_id + '","{#NVRID}":"' + deviceList[i] + '"')
        jsondeviceid = jsondevicefind + '},' + jsondeviceid

jsondeviceid = jsondeviceid[0:-1]
print('{"data":[' + jsondeviceid + ']}')

# ToDo (аналоговые камеры живут тут)
# http://192.168.5.196/ISAPI/System/Video/inputs/channels