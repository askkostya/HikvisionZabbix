import requests
from xml.etree import cElementTree as ET
import readinifile as readini
import time


def getConnection(devicename, namespace):
     try:
         r = requests.get('http://' + readini.getip(devicename) + namespace,auth=(readini.getlogin(devicename), readini.getpassword(devicename)), stream=True)
         xmlstring = r.text
         root = ET.fromstring(xmlstring)
         return root
     except requests.exceptions.RequestException:
         return -1


def get_xmltext_fromdevice(devicename, namespace):
    i = 1
    while i < 5:
        hikdata = getConnection(devicename, namespace)
        if hikdata != -1:
            return hikdata
        time.sleep(5)
        i = i+1
    return 'No route to host'
