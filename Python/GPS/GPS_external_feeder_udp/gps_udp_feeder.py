
import re, time, socket

def Feed_GPS_Data(file_name):

    RMC_TIMESTAMP = r"^(\$GPRMC),[0-9]{6}\.[0-9](,.*)$"
    RMC_DATESTAMP = r"^(\$GPRMC,.*),,[0-9]{6},,,([AV]\*..)$"
    GGA_TIMESTAMP = r"^(\$GPGGA),[0-9]{6}\.[0-9](,.*)$"
    SENTENCE_CHECKSUM = r"^(\$.*)\*..$"
    rmcTS = re.compile( RMC_TIMESTAMP )
    rmcDS = re.compile( RMC_DATESTAMP )
    ggaTS = re.compile( GGA_TIMESTAMP )
    sentCS = re.compile( SENTENCE_CHECKSUM )
    # recalculate the checksum in an NMEA sentence
    def updateChecksum( sentence ):
        checksum = 0
        # don't checksum starting $, 2 digit checksum or prefix char
        for i in range( 1, len( sentence ) - 4 ):
            checksum = checksum ^ ord( sentence[i] )
        checksum = checksum & 0xFF
        newsentence = sentCS.sub( "\\1*%02X" % checksum, sentence )
        return newsentence

    port = 5068
    ip='20.1.100.1'
    # open socket
    try:
        gpsSimSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        gpsSimSock.bind(('', 0))
        gpsSimSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        gpsSimSock.settimeout(150.0)
    except socket.error as e:
        print(e)
        exit(2)


    # init time to just before now
    lastSent = time.time() - 1.0
    content = None;
    # read line
    with open(file_name, 'r') as cooked_file:
        content = cooked_file.readlines()
    gpsSentences = [x.strip() for x in content]

    # while !EOF
    for gpsSentence in gpsSentences:
        # if GGA
        # if( -1 != gpsSentence.find( "GPGGA" ) ):
        #     # wait until 1s since last GGA sent
        #     sleeptime = ( lastSent + 1.0 ) - time.time()
        #     if( 0 < sleeptime) :
        #         time.sleep( sleeptime )
        #     # increment timestamp
        #     lastSent = time.time()
        #     sentenceTimestamp = time.strftime( "\\1,%H%M%S.0\\2", time.gmtime() )
        #     sentenceDatestamp = time.strftime( "\\1,,%d%m%y,,,\\2", time.gmtime() )
        #     # update timestamp in sentence
        #     gpsSentence = ggaTS.sub( sentenceTimestamp, gpsSentence )
        #     # update checksum for new time
        #     gpsSentence = updateChecksum( gpsSentence )
        # elif( -1 != gpsSentence.find( "GPRMC" ) ):

        #     # update timestamp and datestamp in sentence
        #     gpsSentence = rmcTS.sub( sentenceTimestamp, gpsSentence )
        #     gpsSentence = rmcDS.sub( sentenceDatestamp, gpsSentence )
        #     # update checksum for new time&date
        #     gpsSentence = updateChecksum( gpsSentence )

        # send sentence
        print(gpsSentence)
        gpsSimSock.sendto( gpsSentence + "\r\n", ( ip, port ) )
        time.sleep(1)

    #close the socket
    gpsSimSock.close()

Feed_GPS_Data("data.txt")