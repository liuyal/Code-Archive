import time, datetime, sys, os, shutil, parser

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
        recordingsteps = timedownsample * 1 #20

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
        try:
            coordinate = message[index].split('.')
            seconds = float(coordinate[1])
            indexmins = len(coordinate[0]) - 2
            degs = float(coordinate[0][:indexmins])
            mins = float(coordinate[0][indexmins:])
        except: return -1

        result =  ((seconds / 100000 + mins) / 60 + degs) - (0.5 / (60 * 100000))

        return result
    else:
        return -1

def extractData(logFilepath):
    """
    This function extracts all info from log file by parsing NMEA messages.
    :param logFilepath: path of the log file.
    :return: GPS Data
    """

    GPS_Data = []

    # go through all NMEA messages, extract and parse the ones of interest.
    # Make change in here to read new messages.
    with open(logFilepath, 'r') as logfile:
        reader = logfile.readlines()
        for message in reader:
            if 'GGA' in message:
                indexStar = message.rfind('*')
                GPS_Data.append(message[7:indexStar - 1])

    return GPS_Data

def extractLocationInfo(data, latindex, lonindex, type=""):

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

        if type == "DDM":
            if message[latindex] or  message[lonindex] != "":

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
            if message[latindex] or message[lonindex] != "":
                lat = message[latindex]
                lon = message[lonindex]
                if abs(float(lat)) > 0.0 and abs(float(lon)) > 0.0:
                    pointsLatlist.append(lat)
                    pointsLonlist.append(lon)

    return pointsLatlist, pointsLonlist

def Save_output(NMEA_sentences, folder_name):
    output_folder = "output_logs"
    if os.path.exists(os.getcwd() + os.sep + output_folder) != True: os.mkdir(os.getcwd() + os.sep + output_folder)

    output_path = os.getcwd() + os.sep + output_folder + os.sep + folder_name
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.mkdir(output_path)

    for keys in NMEA_sentences.keys():
        file_id = open(output_path + os.sep + keys + ".txt", "w")
        file_id.truncate(0)
        for line in NMEA_sentences[keys]: file_id.write(line + '\n')
        file_id.close()

if __name__ == "__main__":

    input_fd = "input_logs"
    folders = os.listdir(os.getcwd() + os.sep + input_fd)
    try: folders.pop(folders.index("old"))
    except: None;

    for i in range(0,len(folders)): print ( "[" + str(i) + "] " + folders[i])
    print('Enter index:')
    index = input()
    folder_name = folders[int(index)]

    files = sorted(os.listdir(os.getcwd() + os.sep + input_fd + os.sep + folder_name))
    log = []
    for item in (files):
        with open(os.getcwd() + os.sep + input_fd + os.sep + folder_name + os.sep + item, "r") as f_id: text = f_id.read().split('\n')
        log = log + text

    NMEA_sentences = {}
    for line in log:
        msg = line.split(',')
        if '$' in msg[0]:
            msg[0] = msg[0].replace('$','')
        if msg[0] not in NMEA_sentences and msg[0] != "":
            NMEA_sentences[msg[0]] = []
            NMEA_sentences[msg[0]].append(line)
        elif msg[0] != "":
            NMEA_sentences[msg[0]].append(line)

    del line,msg,input_fd,f_id,folders,files,i,item,text

    Save_output(NMEA_sentences, folder_name)

    print("<Parse Complete>")

    input_fd = "output_logs"
    folders = os.listdir(os.getcwd() + os.sep + input_fd)
    try: folders.pop(folders.index("old"))
    except: None;

    folder_name = folders[int(index)]

    logFilePath = os.getcwd() + os.sep + input_fd + os.sep + folder_name + os.sep + "GPGGA.txt"

    outputFolderpath = "output_kml"
    if os.path.exists(os.getcwd() + os.sep + outputFolderpath) != True: os.mkdir(os.getcwd() + os.sep + outputFolderpath)
    output_path = os.getcwd() + os.sep + outputFolderpath + os.sep + folder_name
    if os.path.exists(output_path): shutil.rmtree(output_path)
    os.mkdir(output_path)

    gpsData = extractData(logFilePath)

    gpsLatlist, gpslonlist = extractLocationInfo(data=gpsData, latindex=1, lonindex=3,type='DDM')
    writeToKml(kmlfilepath=os.path.join(output_path, 'gps_points'), latList=gpsLatlist, lonList=gpslonlist,type='gpsData')
    writeToKMLLine(kmlfilepath=os.path.join(output_path, 'gps'), latList=gpsLatlist, lonList=gpslonlist,type='gpsData')

    print("<KML Created>")