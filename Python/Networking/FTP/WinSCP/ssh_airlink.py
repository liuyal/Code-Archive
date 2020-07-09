################################################################################
# This class provides basic methods for ssh operations.
# Company: Sierra Wireless
# Time   : Jun 11, 2013
# Author : Airlink 
# History: 
#          Apr 21, 2014  added int() to port in __init__()
#          Jul 10, 2014 
#                      changed command() and added
#                      invoke_shell()/shell_command()/ssh_key()
################################################################################

import logging
import paramiko
from paramiko.ssh_exception import SSHException
import inspect
import time


class SshAirlink:
    """SshAirlink provides a SSH connection with default connection parameters.
    
    Attributes:
    hostname: Host ip address. Default ip is 192.168.13.31.
    port: Port connection number. Default port number is 22.
    username: Host username. Default username is user.
    password: Connection password. Default is 12345.
    """

    def __init__(self, hostname="192.168.13.31", port="22",\
        username="user", password="12345"):
        """Initializes the connection parameters.
        
        Args:
        hostname: Host ip address. Default ip is 192.168.13.31.
        port: Port connection number. Default port number is 22.
        username: Host username. Default username is user.
        password: Connection password. Default is 12345.
        
        Returns:
        No returns.
        """
        self.hostname = hostname
        self.port = int(port)
        self.username = username
        self.password = password  
              
    def connect(self):
        """Initiates a SSH connection by using parmiko.SSHClient module.
    
        Args:
        No args. 

        Returns:
        True: If the connection set up successfully.
        False: If the connection set up failed.
        """
        logging.info("connecting")
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.hostname, port=self.port,\
                username=self.username, password=self.password)
            
        except Exception, e:
            logging.critical('*** Caught exception: %s: %s' % (e.__class__, e))
            logging.critical("connection failed")
            return False
            
        return True
    
    def command(self, cmd):
        """ Sends a command to the host and returns the response.
         
        Args:
        The cmd is a string without the newline, "\\n", and contains the
        command. 
 
        Returns:
        It returns None if the command is not correct.
        Otherwise, it returns a list of strings that each string is
        terminated with a newline character.
        """
 
        try:
            rcved_list = []
             
            shell = self.ssh.invoke_shell()
             
            timeout = 10
            start_time = time.time()
             
            while True:
                if shell.recv_ready():
                    buf1 = shell.recv(0xFFFF)
                    shell.send(cmd+"\r")
                    time.sleep(2)
                    rcved_list = shell.recv(0xFFFF).split('\n')
                    time.sleep(1)
                    break
                 
                if time.time() - start_time > timeout:
                    self.error_flag+=1
             
        except Exception, e:
            logging.debug("unable to execute command")
            return None
         
        return rcved_list

    def command_v1(self, cmd):
        """ Sends a command to the host and returns the response.
        
        Args:
        The cmd is a string without the newline, "\\n", and contains the
        command. 

        Returns:
        It returns None if the command is not correct.
        Otherwise, it returns a list of strings that each string is
		terminated with a newline character.
        """     
        
        if self.username == "user": 
            rcved_list = []
            try: 
                shell = self.ssh.invoke_shell()
        
                timeout = 10
                start_time = time.time()
                
                while True:
                    if shell.recv_ready():
                        buf1 = shell.recv(0xFFFF)
                        shell.send(cmd+"\r")
                        time.sleep(2)
                        #rcved_list = shell.recv(0xFFFF).split('\n')
                        rcved_list = shell.recv(0xFFFF)
                        logging.debug("received_list:"+str(rcved_list))
                        time.sleep(1)
                        break
        
                    if time.time() - start_time > timeout:
                        self.error_flag+=1
            except:
                logging.debug("unexpected exception catch")
                return None
                         
            return rcved_list
        
        elif self.username == "root": 
            try:
                # ba.cslog("Debug Point => 82")
# # # #                 shell1 = self.ssh.invoke_shell()
# # # #                 ba.cslog("Debug Point => 82-a")
# # # #                 var1=self.shell_command(self, cmd, shell1)
# # # #                 ba.cslog("Debug Point => 82-b")
# # # #                 ba.cslog(var1)
# # # #                 ba.cslog("Debug Point => 82-b")
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
# # # #                ba.cslog("Debug Point => 83")
          
            except SSHException:
                # ba.cslog("unable to execute command")
                logging.debug("unable to execute command")
                return None
            
            except:
                logging.debug("unexpected exception in (" + inspect.stack()[0][3] + ")")
                return None
            
            # ba.cslog("Debug Point => 84")
            stdout_list = stdout.readlines()
            # ba.cslog("Debug Point => 85")
            stderr_list = stderr.readlines()
            # ba.cslog("Debug Point => 86")
            
            if stderr_list:
                # ba.cslog("Debug Point => 87")
                # ba.cslog("bad command:" + "".join(stderr_list))
                logging.debug("bad command:" + "".join(stderr_list))
                return None
 
# # # #            ba.cslog("good command:" + "".join(stdout_list))   
            return stdout_list
    
    def start_command(self, cmd):
        '''
        Sends a command to the host and returns the shell.
        
        Args:
        The cmd is a string without the newline, "\\n", and contains the
        command. 

        Returns:
        It returns False if the command is not correct.
        Otherwise, it returns the shell in use.
        '''
        try:             
            shell = self.ssh.invoke_shell()
        
            timeout = 10
            start_time = time.time()
            
            while True:
                if shell.recv_ready():
                    shell.send(cmd+"\r")
                    time.sleep(2)
                    break
    
                if time.time() - start_time > timeout:
                    return False
                 
        except Exception, e:
            logging.debug("unable to execute command, exception occured: "+str(e))
            return False
         
        return shell
    
    def read_output(self, shell):
        '''
        Reads from the shell given.
        
        Args:
        shell is the shell which has already been 
        opened and in use. 

        Returns:
        It returns the output from the shell screen.
        '''
        return shell.recv(0xFFFF)
            
    def end_command(self, shell):
        '''
        Ends the command from running and reads from 
        the shell given.
        
        Args:
        shell is the shell which has already been 
        opened and in use.
        
        Returns:
        It returns the output from the shell screen.
        '''
        try:
            rcved_list = []

            shell.send("\x03\r")
            time.sleep(2)
            rcved_list = shell.recv(0xFFFF)
            time.sleep(1)
               
        except Exception, e:
            logging.debug("unable to execute command - \x03\r, exception occured: "+str(e))
            return False
        return rcved_list
        
    def close(self):
        """Close the SSH connection.
        It is very important to close the connection before exiting the scripts.

        Args:
        No args. 

        Returns:
        No returns.
        """
        logging.info("closing connection")
        self.ssh.close()


    def invoke_shell(self):
        """ Starts a new shell after SSH connection has been established.
        Useful when testcases require working with a single SSH session
        
        Args:
            None.
        
        Returns:
            The newly created shell
        """
        shell = self.ssh.invoke_shell()
        return shell
    
    def shell_command(self, cmd, shell):
        """ Sends a command to the shell and returns the response.
        Useful when testcases require working with a single SSH session
        
        Args:
        The cmd is a string without the newline, "\\n", and contains the
        command.
        The shell should have been created by invoke_shell
        
        Returns:
        It returns None if the command is not correct.
        Otherwise, it returns a list of strings that each string is
        terminated with a newline character.
        """
        try:
            rcved_list = []
            
            timeout = 10
            start_time = time.time()
            
            while True:
                if time.time() - start_time > timeout:
                    shell.send(cmd+"\r")
                    time.sleep(2)
                    rcved_list = shell.recv(0xFFFF).split('\n')
                    time.sleep(1)
                    if (len(rcved_list) == 0):
                        self.error_flag+=1
                    break
        
        except Exception, e:
            logging.debug("unable to execute command")
            return None
        
        return rcved_list
    
    def ssh_key(self):
        """Return the server SSH key
        Returns the SSH session's server key
        
        Args:
        No args. 
        
        Returns:
        No returns.
        """
        return self.ssh.get_host_keys()