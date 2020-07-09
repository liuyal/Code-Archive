import os
import sys


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
    """
    This function writes the location data to a google earth kml.
    :param kmlfilepath: the path of the ouput kmlfilepath.
    :param latList: Latitude list extracted from GPS data.
    :param lonList: Longitude list extracted from GPS data.
    """

    if type == 'gpsData':
        color = 'ffff0000'
    elif type == 'tpnData':
        color = 'ff0000ff'
    else:
        color = 'ff00ffff'

    recordingsteps = 0

    if timedownsample > 0:
        recordingsteps = timedownsample * 20

    KML = open(kmlfilepath + ".kml", "w")
    KML.write(
        '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">\n')
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
               writePlacemark(KML,str(latList[i]), str(lonList[i]), i)
        else:
            writePlacemark(KML, str(latList[i]), str(lonList[i]), i)

    KML.write('</Folder>\n')
    KML.write('</Document></kml> \n')
    KML.close()

def writeToKMLLine(kmlfilepath, latList=[], lonList=[], type='gpsData', timedownsample=0):
    """
    This function down samples and writes location data in a linestring kml file.
    :param kmlfilepath: the output kml file path.
    :param latList: list containing latitude of all points to be written in the kml file.
    :param lonList: list containing longitude of all points to be written in the kml files.
    :param type: type of the data to write (gpsData or not)
    :param timedownsample: desired frequency in seconds.
    """

    kml = open(kmlfilepath + ".kml", "w")
    # set the trajectory color depending on the the type of the data to write in the kml file.
    if type == 'gpsData':
        color = 'ffff0000'
    elif type == 'tpnData':
        color = 'ff0000ff'
    else:
        color = 'ff00ffff'

    recordingsteps = 0

    if timedownsample > 0:
        recordingsteps = timedownsample * 20

    kml.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name></name>'
              '<description></description><Style id="yellowLineGreenPoly"><LineStyle><color>%s</color><width>3</width>'
              '</LineStyle><PolyStyle><color>%s</color></PolyStyle></Style><Style id="PointStyle"><IconStyle>'
              '<color>%s</color><scale>0.5</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_square.png</href>'
              '</Icon></IconStyle><LabelStyle><scale>0</scale></LabelStyle></Style><Folder><name>Absolute Extruded</name>'
              '<description></description><visibility>1</visibility><open>0</open><Placemark><name>Absolute Extruded'
              '</name><description></description><styleUrl>#yellowLineGreenPoly</styleUrl><LineString><extrude>1</extrude>'
              '<tessellate>1</tessellate><coordinates>\n' % (color, color, color))

    for i in range(len(latList)):
        if timedownsample > 0:
            # perform downsampling of the gpsData mainly (usually).
            if i % recordingsteps == 0:
                kml.write('%s,%s\n' % (lonList[i], latList[i]))
        else:
            kml.write('%s,%s\n' % (lonList[i], latList[i]))

    kml.write('</coordinates></LineString></Placemark></Folder></Document></kml>')

    kml.close()

def getCoordinates(message, index):

    """
    This functions converts deg, minutes and seconds coordinates coordinates into decimal latitude and longitude
    :param message: NMEA message to parse.
    :param index: the coordinate index in the NMEA message.
    :return: calculated coordinate.
    """

    if float(message[index]) > 0.0:
        coordinate = message[index].split('.')
        seconds = float(coordinate[1])
        indexmins = len(coordinate[0]) - 2
        degs = float(coordinate[0][:indexmins])
        mins = float(coordinate[0][indexmins:])

        return ((seconds / 100000 + mins) / 60 + degs) - (0.5 / (60 * 100000))
    else:
        return -1


def extractData(logFilepath):
    """
    This function extracts all info from log file by parsing NMEA messages.
    :param logFilepath: path of the log file.
    :return: TPN, GPS, and Posdata
    """

    PVTData = []
    TPNData = []
    posData = []

    # go through all NMEA messages, extract and parse the ones of interest.
    # Make change in here to read new messages.
    with open(logFilePath, 'r') as logfile:
        reader = logfile.readlines()
        for message in reader:
            if 'PSIWMPVT' in message:
                indexStar = message.rfind('*')
                PVTData.append(message[10:indexStar - 1])
            elif 'PSIWMTPN' in message:
                varList = message.split(',')
                navigationStatus = int(varList[14])
                if navigationStatus >= 1:
                    indexStar = message.rfind('*')
                    TPNData.append(message[10:indexStar - 1])
            elif 'PSIWMPOS' in message:
                indexStar = message.rfind('*')
                posData.append(message[10:indexStar - 1])

    return PVTData, TPNData, posData


def extractLocationInfo(data, latindex, lonindex, type="pvtData"):

    """
    This function parses the PVT, TPN and POS messages, and extracts the GPS, TPN and pos latitude and longitude.
    :param data: data to parse
    :param latindex: index of latitude info in the NMEA message.
    :param lonindex: index of longitude info in the NMEA message
    :param type: type of message (i.e. gps, TPN or Pos data)
    :return: Tow lists containing the the GPS/TPN solution points' latitude and longitude
    """

    pointsLatlist = []
    pointsLonlist = []

    for message in data:
        message = message.split(',')
        if type == 'posData':

            lat = getCoordinates(message, latindex)
            lon = getCoordinates(message=message, index=lonindex)

            if lat != -1 and lon != -1:
                if message[latindex + 1] == 'N':
                    pointsLatlist.append(lat)
                else:
                    pointsLatlist.append(-1 * lat)

                if message[lonindex + 1] == 'E':
                    pointsLonlist.append(lon)
                else:
                    pointsLonlist.append(-1 * lon)
        else:
            lat = message[latindex]
            lon = message[lonindex]
            if abs(float(lat)) > 0.0 and abs(float(lon)) > 0.0:
                pointsLatlist.append(lat)
                pointsLonlist.append(lon)

    return pointsLatlist, pointsLonlist

if __name__ == "__main__":

    try:
        import pydevd

        DEBUGGING = True
    except ImportError:
        DEBUGGING = False
    if DEBUGGING == True:
        logFilePath = r'\\cayyc-share01\users\Sierra\2016_10_Tests\Oct12\2016_10_12_15_10_00_Jeep_KC_OBDII_SmokeTest\recvnmea_20161012_151205.log'
        outputFolderName= 'output_omar'
    else:
        numArguments =  len(sys.argv)
        if numArguments < 2:
            print("[ERROR] Number of arguments is " + str(numArguments) + " instead of 3")
            print("Usage: python Kml_Creator.py [log file path between double quote] [output Folder Name]")
            print("The output folder name is optional, and if not specified the kml files will be created in the log file folder.")
            exit()

        argsList = sys.argv
        logFilePath = argsList[1]
        outputFolderName = ''



        if numArguments == 3:
            outputFolderName = argsList[2]

    logFileFolder, _ = os.path.split(logFilePath)
    if outputFolderName != '':
        outputFolderpath = os.path.join(logFileFolder, outputFolderName)
    else:
        outputFolderpath = logFileFolder

    # create the output folder
    if not os.path.isdir(outputFolderpath):
        os.mkdir(outputFolderpath)

    # extract GPS, TPN and POS messages and load in memory
    gpsData, tpnData, posData = extractData(logFilePath)

    # write GPS Kml.
    gpsLatlist, gpslonlist = extractLocationInfo(data=gpsData, latindex=3, lonindex=4, type='pvtData')
    writeToKml(kmlfilepath=os.path.join(outputFolderpath,'gps_points'),latList=gpsLatlist, lonList=gpslonlist, type='gpsData')
    writeToKMLLine(kmlfilepath=os.path.join(outputFolderpath,'gps'), latList=gpsLatlist, lonList=gpslonlist, type='gpsData')

    # write Nav Kml.
    tpnlatlist, tpnlonlist = extractLocationInfo(data=tpnData, latindex=1, lonindex=2, type="tpnData")
    writeToKml(kmlfilepath=os.path.join(outputFolderpath, 'nav_points'), latList=tpnlatlist, lonList=tpnlonlist,
               type='tpnData', timedownsample=1)
    writeToKMLLine(kmlfilepath=os.path.join(outputFolderpath, 'nav'), latList=tpnlatlist, lonList=tpnlonlist,
                         type='tpnData', timedownsample=1)

    # wrtite Pos kml
    poslatlist, poslonlist = extractLocationInfo(data=posData, latindex=1, lonindex=3, type="posData")
    writeToKml(kmlfilepath=os.path.join(outputFolderpath, 'sierra_nav_points'), latList=poslatlist, lonList=poslonlist,
               type='posData', timedownsample=0)
    writeToKMLLine(kmlfilepath=os.path.join(outputFolderpath, 'sierra_nav'), latList=poslatlist, lonList=poslonlist,
                         type='posData',timedownsample=0)





