#! /usr/bin/python
#
import urllib2
import requests

endpoint1 = r'http://10.30.31.121/2018-12-01_000-cluster_nodes.log'
endpoint2 = r'https://lpxlvaprd01.isus.emc.com/logviewer/Broadcom_Ltd_Shanghai_China/2018-12-07-005/ifs_phone_home_data/2018-12-01_0000-cluster_nodes.log'
endpoint3 = r'https://www.baidu.com'

response1 = urllib2.urlopen(endpoint1)
response2 = urllib2.urlopen(endpoint2)
response3 = urllib2.urlopen(endpoint3)

# print response1.getcode()
# print response2.getcode()
print response3.getcode()

# html1 = response1.read()
# html2 = response2.read()
html3 = response3.read()

# print "html1: " + html1[:100]
# print "html2: " + html2[:100]
print "html3: " + html3[:100]

