import logging
import time
import sys
import rpyc
import rpyc.utils

class ProxyAirlink:
    """ProxyAirlink class provides a simple connection with default
	connection parameters. In this class all timeout exception are caught to
	prevent termination.
    
    Attributes:
        hostname: Host ip address. Default ip is 192.168.13.31.
        port: Port connection number. Default port number is 2332.
    """
    def __init__(self, ip = "127.0.0.1", port = 18812,\
		debug_mode = True):
        """Initializes the connection parameters.
        
        Args:
            hostname: Host ip address. Default ip is 127.0.0.1.
            This default valued is for local development purpose once launch the
            local proxy server, when the code migrate to the test bed, it will be
            relaced with host IP in testbed configuration file.  
            port: Port connection number. Default port number is 18812.
            debug_mode: Enables the debug mode. Default is True. If it is True,
			all sent and received data are printed out in terminal.
        
        Returns:
            rpyc object if succeed other return exception.
        """
        self.ip = ip
        self.port = port
        self.debug_mode = debug_mode
        print "Proxy object initialization!"
        logging.debug("Controller parameters are initialized")
        self.conn =None
   
    def connect(self):
        """Initiates a connection by using rpyc module.
        
        Args:
            No args. 

        Returns:
            True: If the connection set up successfully, return connect obj.
            False: If the connection set up failed.
        """
        logging.info("Controller connecting to host PC")
        try:
            self.conn = rpyc.classic.connect(self.ip, self.port)
            return self.conn 
        except:
            logging.error("failed to connect to the " +self.ip)
            return False

    def upload(self, localpath, remotepath):
        """Uploads a file or dir using rpyc module.
        
        Args:
            localpath
            remotepath

        Returns:
            True: If the upload succeeded
            False: If the upload failed
        """
        logging.info("Controller uploading file to host PC")
        try:
            rpyc.classic.upload(self.conn, localpath, remotepath)
            return True
        except:
            logging.error("failed to upload file to remote location: " + remotepath)
            return False

    def deliver(self, local_Obj):
        """Send local object by using rpyc module.
        
        Args:
            No args. 

        Returns:
            True: If deliver successfully, return local obj.
            False: If delivery fails, return false.
        """
        logging.info("Controller sending local object to host PC")
        try:
            remote_Obj = rpyc.utils.classic.deliver(self.conn, local_Obj)
            return remote_Obj 
        except:
            logging.error("failed to deliver "+str(type(local_Obj))+" to the " +self.ip)
            return False

    def local_output(self):
        with rpyc.classic.redirected_stdio(self.conn): 
            print "local see"
