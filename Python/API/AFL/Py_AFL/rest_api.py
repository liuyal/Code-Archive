import requests
import json, xml, xml.dom.minidom
import xml.etree.ElementTree as ET


r = requests.get("https://my-json-server.typicode.com/typicode/demo")
dom = xml.dom.minidom.parseString(r.content.decode('utf-8'))
pretty_xml = dom.toprettyxml()
print(pretty_xml)





