import time, os, sys, datetime
import parser


# https://www.gpsinformation.org/dale/nmea.htm
# https://www.pgc.umn.edu/apps/convert/

def writePlacemark(KML, lat, lon, index):
    KML.write('<Placemark>\n')
    KML.write('<name>%s</name>\n' % (index))
    KML.write('<description></description>\n')
    KML.write('<styleUrl>#TrajPointStyle</styleUrl>\n')
    KML.write('<visibility>1</visibility>\n')
    KML.write('<Point>\n')
    KML.write('<coordinates>\n')
    KML.write('%s , %s\n' % (lon, lat))
    KML.write('</coordinates>\n')
    KML.write('</Point>\n')
    KML.write('</Placemark>\n')


def writeToKml(kmlfilepath, latList, lonList, type, timedownsample=0):

    if type == 'gpsData':
        color = 'ff000000'
    elif type == 'tpnData':
        color = 'ff000000'
    else:
        color = 'ff000000'

    recordingsteps = 0

    if timedownsample > 0: recordingsteps = timedownsample * 20

    KML = open(kmlfilepath + ".kml", "w")
    KML.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
    KML.write('<Document>\n')
    KML.write('<name>Output Trajectory</name>\n')
    KML.write('<description></description>\n')
    KML.write('<open>1</open>\n')
    KML.write('<Style id="TrajLineStyle">\n')
    KML.write('<LineStyle>\n')
    KML.write('<color>ff000000</color>\n')
    KML.write('<width>3</width>\n')
    KML.write('</LineStyle>\n')
    KML.write('<PolyStyle>\n')
    KML.write('<color>%s</color>\n' % color)
    KML.write('</PolyStyle>\n')
    KML.write('</Style>\n')
    KML.write('<Style id="TrajPointStyle">\n')
    KML.write('<IconStyle>\n')
    KML.write('<color>%s</color>\n' % color)
    KML.write('<scale>0.5</scale>\n')
    KML.write('<Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_square.png</href></Icon>\n')
    KML.write('</IconStyle>\n')
    KML.write('<LabelStyle>\n')
    KML.write('<color>%s</color>\n' % color)
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
                writePlacemark(KML, str(latList[i]), str(lonList[i]), i)
        else:
            writePlacemark(KML, str(latList[i]), str(lonList[i]), i)

    KML.write('</Folder>\n')
    KML.write('</Document></kml> \n')
    KML.close()


if __name__ == "__main__":
    f = open("bus_info.csv", "r")
    txt = f.readlines()
    f.close()

    gpsLatlist = []
    gpslonlist = []

    for item in txt[1:]:
        gpsLatlist.append(float(item.split(',')[6]))
        gpslonlist.append(float(item.split(',')[7]))

    writeToKml(kmlfilepath=os.path.join(os.getcwd(), 'gps_points'), latList=gpsLatlist, lonList=gpslonlist, type='gpsData')
