#!/opt/local/bin/python2.7

#  swipoll.py
#  
#
#  Created by Scott Ripley on 10/21/15.
#
#
import os
import re
import inspect
import pwd
import sys
import subprocess
import time
import xml.sax
import pprint
from xml.dom import minidom
from xml.dom.minidom import parse, parseString
import xmltodict
import xml.etree.ElementTree as ET
import paramiko
#from lxml import etree
from io import StringIO, BytesIO

# Files & Paths
dirpath = os.getcwd()
xmlpath = dirpath + "/item.xml"
configfile = dirpath + "/config.data"
xml_file = dirpath + "/show_int.xml"
xml_out = dirpath + "/out.xml"

# XML Formats

hello = """<?xml version="1.0" encoding="ISO-8859-1"?>
    <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <capabilities>
    <capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    </capabilities>
    <session-id>9605</session-id>
    </hello>
    ]]>]]>"""

xml_hed = """<?xml version="1.0" encoding="ISO-8859-1"?>"""
hello_hed = "<hello"
hello_end = "]]>]]>"


def pollit(switch, xml_file, outfile):
    
    print xml_file, " & ", outfile
    xmldest = open(outfile, 'wb')
    xmlout = subprocess.Popen(['cat', xml_file ], stdout=subprocess.PIPE)
    sshout = subprocess.Popen(['ssh', '-2A', switch, '-s', 'xmlagent'], stdin=xmlout.stdout, stdout=xmldest)
    sshout.wait()
    xmldest.close()


# Main

inspect.getfile(os)

# Abstract out config data here
with open(configfile,'rU') as configdata:
    for line in configdata:
        line = line.rstrip()
        a = line.split(",")
        
        if a[0] == "SWITCH":
            print "Switch = ", a[1]
            switch = a[1]
        elif a[0] == "ACCOUNT":
            print "Account = ", a[1]
            account = a[1]
        elif a[0] == "PASSWORD":
            print "Password = ", a[1]
            password = a[1]

pollit(switch, xml_file, xml_out)

print("\n################################\n\n\n")
xsd_src = open('netconf.xsd','rb')

with open(xml_out, 'r') as file:
    xml_data = file.read()

#print xml_data
xml_lines = xml_data.split('\n')

for i, line in enumerate(xml_lines, start=0):
    
    if hello_end in line:
        break
    else:
        continue

clean_xml = []

for line in xml_lines[i:]:
    
    if hello_end in line:
        nline = line.replace(']]>]]>','',1)
    else:
        nline = line
    
    # print "LINE: ", nline
    clean_xml.append(nline)



xml_data = '\n'.join(clean_xml)
# print xml_data
dom = parseString(xml_data)
xml = dom.toprettyxml()
# print(xml)

ns = {'mod': 'http://www.cisco.com/nxos:1.0:if_manager',
    'nxos': 'http://www.cisco.com/nxos:1.0'}

root = ET.fromstring(xml_data)
ET.dump(root)
# root = tree.getroot()
# ET.dump(root)
# print root.findall(".//mod:interface", namespaces=ns)

for interface in root.findall('.//mod:ROW_interface', namespaces=ns):
    vlan = interface.find('.//mod:vlan', ns)
    speed = interface.find('.//mod:speed', ns)
    int = interface.find('.//mod:interface', ns)
#print "Interface: ",int.text
#print " VLAN: ",vlan.text, "Speed: ", speed.text

for interface in root.findall('.//mod:ROW_interface', namespaces=ns):
    for int_config in interface.iter():
        short_int = int_config.tag.split('}', 1)
        # int_config.tag = int_config.tag[len(ns['mod'])]
        print short_int[1],"\t ",int_config.text


exit(0)

