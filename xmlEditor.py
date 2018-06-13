import csv, sys, string
import arcpy
import cookielib
from cookielib import CookieJar
import urllib2
from urllib2 import urlopen
import difflib
import re
from re import sub
from arcpy import env
from xml.dom import minidom
import xml.dom.minidom
import smtplib

#Open web page with xml data
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')]
#Get publication date from xml web page
sourceCode = opener.open('https://prd-tnm.s3.amazonaws.com/StagedProducts/Hydrography/NHD/State/HighResolution/GDB/NHD_H_Nevada_State_GDB.xml').read()
splitSource = re.findall(r'<pubdate>(.*?)</pubdate>',sourceCode)
for item in splitSource:
    pubdate = re.sub(r'<.*?>','',item)
print pubdate

#Make sde Connection 
sde_conn = "####"
arcpy.env.workspace = sde_conn
#fcList = arcpy.ListFeatureClasses()
#for fc in fcList:
#    print fc


#Create xml file of metadata
dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
translator = dir + "Metadata/Translator/ArcGIS2ISO19139.xml"
date = time.strftime('%Y%m%d%I%M%S')
xmlFile = "#####" + date + ".xml"
arcpy.ExportMetadata_conversion(sde_conn, translator, xmlFile)

#Parse the xml file
myxml = minidom.parse(xmlFile)
purpose = myxml.getElementsByTagName("purpose")[0]
document = purpose.getElementsByTagName("gco:CharacterString")[0].firstChild.data
date = re.findall(r'\d\d\d\d\d\d\d\d',document)
for item in date:
    metaDate = ''
    metaDate += item
print metaDate

#If data is updated print "Data up-to-date"
#If data is outdated send email 
if metaDate == pubdate:
    print "Data up to date"
else:
    fromAddr = "gis@dot.nv.gov"
    toAddr = "mlemmon@dot.nv.gov"

    subject = "DEVReference data outdated"
    finish_time = time.asctime()
    current_time = time.asctime()
    msgBody = "Data on DEVReference is outdated"

    msg = string.join(("From: %s" %fromAddr, "To: %s" %toAddr, "Subject: %s" %subject, "", msgBody),"\r\n")

    server = smtplib.SMTP('WEBSMTP', 25)
    server.sendmail(fromAddr,toAddr,msg)
    server.quit()


