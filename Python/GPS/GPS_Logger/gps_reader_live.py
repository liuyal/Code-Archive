import time, os, sys, datetime

inmotionautomation_home_dirname = os.environ['INMOTIONAUTOMATION_HOME']
sys.path.append(inmotionautomation_home_dirname + "\lib\common")

import mg_connection_wd

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

        # result =  ((seconds / 100000 + mins) / 60 + degs) - (0.5 / (60 * 100000))

        result = degs + (mins + (seconds/10000))/60

        return result
    else:
        return -1

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
        if message[latindex] != "" and  message[lonindex] != "":

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

    return pointsLatlist, pointsLonlist

output_path = r"C:\Users\jerliu\OneDrive - Sierra Wireless, Inc\Desktop\Jerry\4. Training\Python_Training\Google_Earth_test\output"
output_folder = "output"
GGA_out = "GGA_ouput.txt"

clear_history = False

logFilePath = output_path + "\\" + GGA_out

GGA_out_id = open(logFilePath, "r")
st_results = os.stat(logFilePath)
st_size = st_results[6]
GGA_out_id.seek(st_size)

xml_string ="""
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
<Placemark>
    <name>TT</name>
    <description>Live Update</description>
    <Point>
    <coordinates>%s,%s,0</coordinates>
    </Point>
</Placemark></kml>"""

xml_header = r'''<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name></name>
<description></description><Style id="yellowLineGreenPoly"><LineStyle><color>%s</color><width>3</width>
</LineStyle><PolyStyle><color>%s</color></PolyStyle></Style><Style id="PointStyle"><IconStyle>
<color>%s</color><scale>0.5</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_square.png</href>
</Icon></IconStyle><LabelStyle><scale>0</scale></LabelStyle></Style><Folder><name>Absolute Extruded</name>
<description></description><visibility>1</visibility><open>0</open><Placemark><name>Absolute Extruded
 </name><description></description><styleUrl>#yellowLineGreenPoly</styleUrl><LineString><extrude>1</extrude><tessellate>1</tessellate><coordinates>'''
xml_tail = "</coordinates></LineString></Placemark></Folder></Document></kml>"

try:
    reader = ""
    with open("position_trace.kml", "r") as infile:
        reader = infile.read()
except:
    print("Read Error")
if "</coordinates>" not in reader or clear_history:
   with open("position_trace.kml", "w") as infile2:
       infile2.truncate(0)
       infile2.write(xml_header + "\n" + xml_tail)

while True:
    time.sleep(1)
    where = GGA_out_id.tell()
    line = GGA_out_id.readline()

    if not line:
        GGA_out_id.seek(where)

    elif line:
        # print(line)  # already has newline
        message = line.split(",")
        gpsLatlist, gpslonlist = extractLocationInfo(data=line, latindex=2, lonindex=4, type='DDM')
        print("Lat: " + str(gpsLatlist) + "| Lon: " + str(gpslonlist))
        try:
            with open("position.kml", "w") as pos:
                pos.write(xml_string % (gpslonlist[0],gpsLatlist[0]))
        except:
            print("ERROR")
        try:
            if str(gpslonlist[0]) != "" or str(gpsLatlist[0]) != "":
                with open("position_trace.kml", "r") as in_file:
                    buf = in_file.readlines()
                with open("position_trace.kml", "w") as out_file:
                    for line in buf:
                        if line == xml_tail:
                            line = str(gpslonlist[0]) + "," + str(gpsLatlist[0]) + "\n" + xml_tail
                        out_file.write(line)
        except:
            print("ERROR")

