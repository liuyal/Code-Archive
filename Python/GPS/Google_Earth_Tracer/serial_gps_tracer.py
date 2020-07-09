import time, os, sys, datetime, serial, traceback

xml_string = """<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2"><Placemark><name>TT</name><description>Live Update</description><Point><coordinates>%s,%s,0</coordinates></Point></Placemark></kml>"""
xml_header = r'<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name></name><description></description><Style id="yellowLineGreenPoly"><LineStyle><color>ffff0000</color><width>3</width></LineStyle><PolyStyle><color>ffff0000</color></PolyStyle></Style><Style id="PointStyle"><IconStyle><color>ffff0000</color><scale>0.5</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_square.png</href></Icon></IconStyle><LabelStyle><scale>0</scale></LabelStyle></Style><Folder><name>Absolute Extruded</name><description></description><visibility>1</visibility><open>0</open><Placemark><name>Absolute Extruded</name><description></description><styleUrl>#yellowLineGreenPoly</styleUrl><LineString><extrude>1</extrude><tessellate>1</tessellate><coordinates>'
xml_tail = "</coordinates></LineString></Placemark></Folder></Document></kml>"


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

        result = ((seconds / 100000 + mins) / 60 + degs) - (0.5 / (60 * 100000))

        # result = degs + (mins + (seconds/10000))/60

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

    message = data.split(',')

    if type == "DDM":
        if message[latindex] != "" and message[lonindex] != "":

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


if __name__ == "__main__":

    serial_com = "COM3"
    br = 9600
    clear_history = True

    connection = serial.Serial(serial_com, baudrate=br, timeout=60)

    msglogfile = open("gps_log.txt", "a")

    infile = open("position_trace.kml", "r")
    reader = infile.read()
    infile.close()

    if "</coordinates>" not in reader or clear_history:
        infile2 = open("position_trace.kml", "w")
        infile2.truncate(0)
        infile2.write(xml_header + "\n" + xml_tail)
        infile2.flush()
        infile2.close()
        msglogfile.truncate(0)

    try:
        while True:
            GGA_sentence = ""
            RMC_sentence = ""

            msg = connection.readline().decode(encoding='UTF-8', errors='ignore').strip()
            msglogfile.write(msg + "\n")
            msglogfile.flush()

            lines = msg.split("\n")

            for i in range(0, len(lines)):
                if "GGA" in lines[i]: GGA_sentence = lines[i]
                if "RMC" in lines[i]: RMC_sentence = lines[i]

            if GGA_sentence != "":
                gpsLatlist, gpslonlist = extractLocationInfo(data=GGA_sentence, latindex=2, lonindex=4, type='DDM')
                print("Lat: " + str(gpsLatlist))
                print("Lon: " + str(gpslonlist))

                pos_kml = open("position.kml", "w")
                pos_kml.write(xml_string % (gpslonlist[0], gpsLatlist[0]))
                pos_kml.flush()
                pos_kml.close()

                if str(gpslonlist[0]) != "" and str(gpsLatlist[0]) != "":
                    in_file = open("position_trace.kml", "r")
                    buf = in_file.readlines()
                    in_file.close()

                    out_file = open("position_trace.kml", "w")
                    for line in buf:
                        if line == xml_tail:
                            line = str(gpslonlist[0]) + "," + str(gpsLatlist[0]) + "\n" + xml_tail
                        out_file.write(line)
                    out_file.flush()
                    out_file.close()

    except Exception as e:
        traceback.print_exc()
        print("ERROR: " + str(e))
        msglogfile.close()