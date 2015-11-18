#!/usr/bin/python

import os
import re
import inspect
import pwd
import sys
import subprocess
import time
import xml.sax
import pprint
import json
import requests
from xml.dom import minidom
from xml.dom.minidom import parse, parseString
#import xmltodict
import xml.etree.ElementTree as ET
import paramiko
#from lxml import etree
from io import StringIO, BytesIO

dir_prefix = "/home"
#dir_prefix = "/Users"

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

inspect.getfile(os)
switch = "SWITCH
xml_file = dir_prefix + "/scripley/xython2.7/xython2.7/show_int.xml"
xml_out = dir_prefix + "/scripley/xython2.7/xython2.7/out.xml"
test_out = dir_prefix + "/scripley/xython2.7/xython2.7/test.xml"

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def xml2data():
    # tree = ET.parse('/Users/scripley/xython2.7/xython2.7/out.xml')
    tree = ET.parse('~/out.xml')
    root = tree.getroot()
    interfaces = root.findall('.')
    content = ""

    for child in root:
        print(child.tag, child.attrib)

def pollit(switch, xml_file, outfile):

    print xml_file, " & ", outfile
    # outfile = open('/Users/scripley/xython2.7/xython2.7/out.xml', 'wb')
    xmldest = open(outfile, 'wb')
    xmlout = subprocess.Popen(['cat', xml_file ], stdout=subprocess.PIPE)
    sshout = subprocess.Popen(['ssh', '-2A', switch, '-s', 'xmlagent'], stdin=xmlout.stdout, stdout=xmldest)
    sshout.wait()
    xmldest.close()

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

#ET.register_namespace("nxos", "http://www.cisco.com/nxos:1.0")
#ET.register_namespace("mod", "http://www.cisco.com/nxos:1.0:if_manager")

#tree = ET.parse('/Users/scripley/xython2.7/xython2.7/out.xml')
#test_tree = ET.parse('/Users/scripley/xython2.7/xython2.7/test.xml')

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

ip=switch

my_headers = {'content-type': 'application/json-rpc'}
url = "http://"+ip+"/ins"
username = "admin"
password = "abc123"


payload=[{"jsonrpc": "2.0",
         "method": "cli",
         "params": {"cmd": "show version",
         "version": 1},
         "id": 1}
         ]

response = requests.post(url, data=json.dumps(payload), headers=my_headers, auth=(username, password)).json()

#Here is the cool part with collecting the info we need from the output
kick_start_image = response['result']['body']['kickstart_ver_str']
chassis_id = response['result']['body']['chassis_id']
hostname =  response['result']['body']['host_name']

print "ip : {0} is a \"{1}\" with hostname: {2} running software version : {3}".format(ip , chassis_id, hostname, kick_start_image)

exit(0)

# schema.validate(xml_tree)

itemlist = xml.getElementsByTagName('ROW_interface')

pp = pprint.PrettyPrinter(indent=4, depth=4)
pp.pprint(itemlist)


exit(0)


user = get_username()
sshconn = paramiko.client.SSHClient()
sshconn.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
sshconn.load_system_host_keys()
print ("Switch is", switch, "UID is ", user, " keys loaded\n")
sshconn.connect(switch,port=22,username=user)
# get a session
s = sshconn.get_transport().open_session()
print ("Session opened.\n")
# set up the agent request handler to handle agent requests from the server
paramiko.agent.AgentRequestHandler(s)  # <--UNDOCUMENTED??!!
# get a shell
sshconn.exec_command('term len 0')
stdin, stdout, stderr = sshconn.exec_command('sh ver')
a=stdout.read()
print (a)
exit(0)


#f = open("/Users/scripley/show_int.xml", 'r')

#for line in f:
#	print(line, "\n")

#This is strictly for proof-of-concept when I forget how to xml things
#xmldoc = minidom.parse('/Users/scripley/xython2.7/xython2.7/item.xml')
#itemlist = xmldoc.getElementsByTagName('item')
#print "Len : ", len(itemlist)
#print "Attribute Name : ", itemlist[0].attributes['name'].value
#print "Text : ", itemlist[0].firstChild.nodeValue
#for s in itemlist :
#    print "Attribute Name : ", s.attributes['name'].value
#    print "Text : ", s.firstChild.nodeValue
#
#exit(0)


#
#print "Len: ", len(itemlist)
#print "Attribute: ", itemlist[0].nodeValue
#print "Text: ",itemlist[0].firstChild.nodeValue
#for s in itemlist :
## print "Text: ", s.firstChild.nodeValue
#    print "Value: ", s[0]
#exit(0)
#
#
#xml_file = "/Users/scripley/show_int.xml"
#outfile = open('/Users/scripley/out.xml', 'wb')
#xmlout = subprocess.Popen(['cat', xml_file ], stdout=subprocess.PIPE)
#sshout = subprocess.Popen(['ssh', '-2A', switch, '-s', 'xmlagent'], stdin=xmlout.stdout, stdout=outfile)
#outfile.close()
#
#infile = open('/Users/scripley/out.xml','r')
#xmldump = infile.read()
#xmltodict.parse(xmldump, item_depth=3)
#exit(0)
#
#for child in root:
#	print(child.tag, child.attrib)
#
#
#exit(0)

#import pip
#    from subprocess import call
#
#for dist in pip.get_installed_distributions():
#    call("pip install --upgrade " + dist.project_name, shell=True)
