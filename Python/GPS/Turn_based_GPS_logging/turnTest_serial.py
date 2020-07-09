import os
import sys, time
import re
import operator


inmotionautomation_home_dirname = os.environ['INMOTIONAUTOMATION_HOME']
sys.path.append(inmotionautomation_home_dirname + "\lib\common")

import mg_connection_wd

def writePlacemark(KML, lat, lon, color, index):
    style = 'TrajPointBlue'
    if "1" in color:
        style = 'TrajPointGreen'

    KML.write('<Placemark>\n')
    KML.write('<name>%s</name>\n' % (index))
    KML.write('<description></description>\n')
    KML.write('<styleUrl>#%s</styleUrl>\n' % (style))
    KML.write('<visibility>1</visibility>\n')
    KML.write('<Point>\n')
    KML.write('<coordinates>\n')
    KML.write('%s , %s\n' % (lon, lat))
    KML.write('</coordinates>\n')
    KML.write('</Point>\n')
    KML.write('</Placemark>\n')

def writeToKml(kmlfilepath, latList, lonList, colList, timedownsample=0):
    """
    This function writes the location data to a google earth kml.
    :param kmlfilepath: the path of the ouput kmlfilepath.
    :param latList: Latitude list extracted from GPS data.
    :param lonList: Longitude list extracted from GPS data.
    """

    recordingsteps = 0

    if timedownsample > 0:
        # recordingsteps = timedownsample * 20
        recordingsteps = timedownsample

    KML = open(kmlfilepath + ".kml", "w")
    KML.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
    KML.write('<Document>\n')
    KML.write('<name>Output Trajectory</name>\n')
    KML.write('<description></description>\n')
    KML.write('<open>1</open>\n')
    KML.write('<Style id="TrajLineStyle">\n')
    KML.write('<LineStyle>\n')
    KML.write('<color>ff0000ff</color>\n')
    KML.write('<width>3</width>\n')
    KML.write('</LineStyle>\n')
    KML.write('<PolyStyle>\n')
    KML.write('<color>ff00ffff</color>\n')
    KML.write('</PolyStyle>\n')
    KML.write('</Style>\n')
    KML.write('<Style id="TrajPointBlue">\n')
    KML.write('<IconStyle>\n')
    KML.write('<color>42f45c</color>\n')
    KML.write('<scale>0.15</scale>\n')
    KML.write('<Icon><href>http://maps.google.com/mapfiles/kml/paddle/blu-blank-lv.png</href></Icon>\n')
    KML.write('</IconStyle>\n')
    KML.write('<LabelStyle>\n')
    KML.write('<color>42f45c</color>\n')
    KML.write('<scale>0</scale>\n')
    KML.write('</LabelStyle>\n')
    KML.write('</Style>\n')
    KML.write('<Style id="TrajPointGreen">\n')
    KML.write('<IconStyle>\n')
    KML.write('<color>e81e3c</color>\n')
    KML.write('<scale>0.15</scale>\n')
    KML.write('<Icon><href>http://maps.google.com/mapfiles/kml/paddle/grn-blank-lv.png</href></Icon>\n')
    KML.write('</IconStyle>\n')
    KML.write('<LabelStyle>\n')
    KML.write('<color>e81e3c</color>\n')
    KML.write('<scale>0</scale>\n')
    KML.write('</LabelStyle>\n')
    KML.write('</Style>\n')
    KML.write('<Folder>\n')
    KML.write('<name>Trajectory</name>\n')
    KML.write('<description></description>\n')
    KML.write('<visibility>1</visibility>\n')
    KML.write('<open>0</open>\n')
    for i in range(len(latList)):
        if timedownsample > 0:
            if i % recordingsteps == 0:
                writePlacemark(KML, str(latList[i]), str(lonList[i]), str(colList[i]), i)
        else:
            writePlacemark(KML, str(latList[i]), str(lonList[i]), str(colList[i]), i)

    KML.write('</Folder>\n')
    KML.write('</Document></kml> \n')
    KML.close()

def extractData(logFilepath):
    """
    This function extracts all info from log file by parsing NMEA messages.
    :param logFilepath: path of the log file.
    :return: TPN, GPS, and Posdata
    """
    gpsData = []
    lineNum = 0

    # go through all NMEA messages, extract and parse the ones of interest.
    # Make change in here to read new messages.
    with open(logFilepath, 'r') as logfile:
        reader = logfile.readlines()
        for message in reader:
            lineNum = lineNum + 1
            gpsData.append(message)

    return gpsData

def extractLocationInfo(data, latindex, lonindex, colorindex):
    """
    This function parses the PVT, TPN and POS messages, and extracts the GPS, TPN and pos latitude and longitude.
    :param data: data to parse
    :param latindex: index of latitude info in the NMEA message.
    :param lonindex: index of longitude info in the NMEA message
    :return: Tow lists containing the the GPS/TPN solution points' latitude and longitude
    """

    pointsLatlist = []
    pointsLonlist = []
    pointsColorlist = []

    for message in data:
        message = message.split(',')
        lat = message[latindex]
        lon = message[lonindex]

        coordinate = lat.split('.')
        seconds = float(coordinate[1])
        indexmins = len(coordinate[0]) - 2
        degs = float(coordinate[0][:indexmins])
        mins = float(coordinate[0][indexmins:])
        lat = ((seconds / 100000 + mins) / 60 + degs) - (0.5 / (60 * 100000))

        coordinate = lon.split('.')
        seconds = float(coordinate[1])
        indexmins = len(coordinate[0]) - 2
        degs = float(coordinate[0][:indexmins])
        mins = float(coordinate[0][indexmins:])
        lon = -1*((seconds / 100000 + mins) / 60 + degs) - (0.5 / (60 * 100000))

        if abs(float(lat)) > 0.0 and abs(float(lon)) > 0.0:
            pointsLatlist.append(lat)
            pointsLonlist.append(lon)
            pointsColorlist.append(message[colorindex])

    return pointsLatlist, pointsLonlist, pointsColorlist


if __name__ == "__main__":

    serial_com = "COM39"
    br = 115200
    my_connection = mg_connection_wd.Serial_Connection(serial_com, br)
    my_connection.connect()
    msglogfile = open("out_log.txt", "w+")
    msglogfile.truncate(0)
    msg = ""

    while True:
        try: msg = my_connection.serial_read(time_window=1)[1].replace('\r','')
        except: None

        line = msg.split('\n')
        for item in line:
            if "GGA" in item:
                print(item)
                msglogfile.write(item+'\n')
                msglogfile.flush()
                gpsData = extractData("out_log.txt")
                gpsLatlist, gpslonlist, colorlist = extractLocationInfo(data=gpsData, latindex=2, lonindex=4, colorindex=2)
                writeToKml(kmlfilepath=os.path.join(os.getcwd(), 'turn_points'), latList=gpsLatlist, lonList=gpslonlist,colList=colorlist)
