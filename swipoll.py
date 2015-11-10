#!/opt/local/bin/python2.7

#  swipoll.py
#  
#
#  Created by Scott Ripley on 10/21/15.
#
#
import os
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

#This is strictly for proof-of-concept when I forget how to xml things
xmldoc = minidom.parse('/Users/scripley/xython2.7/xython2.7/item.xml')
itemlist = xmldoc.getElementsByTagName('item')
#print "Len : ", len(itemlist)
#print "Attribute Name : ", itemlist[0].attributes['name'].value
#print "Text : ", itemlist[0].firstChild.nodeValue
#for s in itemlist :
#    print "Attribute Name : ", s.attributes['name'].value
#    print "Text : ", s.firstChild.nodeValue
#
#
#
#print "Len: ", len(itemlist)
#print "Attribute: ", itemlist[0].nodeValue
#print "Text: ",itemlist[0].firstChild.nodeValue
#for s in itemlist :
## print "Text: ", s.firstChild.nodeValue
#    print "Value: ", s[0]
#exit(0)

switch = "SWITCH"

xml_file = "/Users/scripley/xython2.7/xython2.7/show_int.xml"
outfile = open('/Users/scripley/xython2.7/xython2.7/out.xml', 'wb')
xmlout = subprocess.Popen(['cat', xml_file ], stdout=subprocess.PIPE)
sshout = subprocess.Popen(['ssh', '-2A', switch, '-s', 'xmlagent'], stdin=xmlout.stdout, stdout=outfile)
outfile.close()

infile = open('/Users/scripley/out.xml','r')
xmldump = infile.read()
xmltodict.parse(xmldump, item_depth=3)
exit(0)

for child in root:
	print(child.tag, child.attrib)


exit(0)
