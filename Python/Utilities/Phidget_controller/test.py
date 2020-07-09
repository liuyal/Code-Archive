import sys
import time 
import traceback
from Phidget22.Devices.DigitalOutput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

try:
    from PhidgetHelperFunctions import *
except ImportError:
    sys.stderr.write("\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
                      "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

'''
* Displays info about the attached Phidget channel.
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
'''
def onAttachHandler(self):
    
    ph = self
    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
    
        print("\nAttach Event:")
        
        """
        * Get device information and display it.
        """
        serialNumber = ph.getDeviceSerialNumber()
        channelClass = ph.getChannelClassName()
        channel = ph.getChannel()
        
        deviceClass = ph.getDeviceClass()
        if (deviceClass != DeviceClass.PHIDCLASS_VINT):
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Channel:  " + str(channel) + "\n")
        else:            
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
                  
    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return
"""
* Displays info about the detached Phidget channel.
* Fired when a Phidget channel with onDetachHandler registered detaches
*
* @param self The Phidget channel that fired the attach event
"""
def onDetachHandler(self):

    ph = self
    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
    
        print("\nDetach Event:")
        
        """
        * Get device information and display it.
        """
        serialNumber = ph.getDeviceSerialNumber()
        channelClass = ph.getChannelClassName()
        channel = ph.getChannel()
        
        deviceClass = ph.getDeviceClass()
        if (deviceClass != DeviceClass.PHIDCLASS_VINT):
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Channel:  " + str(channel) + "\n")
        else:            
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        
    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Writes Phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):

    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

"""
* Creates, configures, and opens a DigitalOutput channel.
* Provides interface for setting the duty cycle of the DigitalOutput channel
* Closes out DigitalOutput channel
*
* @return 0 if the program exits successfully, 1 if it exits with errors.
"""
def main():
    try:
        """
        * Allocate a new Phidget Channel object
        """
        ch = DigitalOutput()
        
        """
        * Set matching parameters to specify which channel to open
        """
        #You may remove this line and hard-code the addressing parameters to fit your application
        channelInfo = AskForDeviceParameters(ch)
        
        ch.setDeviceSerialNumber(channelInfo.deviceSerialNumber)
        ch.setHubPort(channelInfo.hubPort)
        ch.setIsHubPortDevice(channelInfo.isHubPortDevice)
        ch.setChannel(channelInfo.channel)   
        
        if(channelInfo.netInfo.isRemote):
            ch.setIsRemote(channelInfo.netInfo.isRemote)
            if(channelInfo.netInfo.serverDiscovery):
                try:
                    Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)
                except PhidgetException as e:
                    PrintEnableServerDiscoveryErrorMessage(e)
                    raise EndProgramSignal("Program Terminated: EnableServerDiscovery Failed")
            else:
                Net.addServer("Server", channelInfo.netInfo.hostname,
                    channelInfo.netInfo.port, channelInfo.netInfo.password, 0)
        
        """
        * Add event handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch.setOnAttachHandler(onAttachHandler)
        
        print("Setting OnDetachHandler...")
        ch.setOnDetachHandler(onDetachHandler)
        
        print("Setting OnErrorHandler...")
        ch.setOnErrorHandler(onErrorHandler)
        
        """
        * Open the channel with a timeout
        """
        
        print("\nOpening and Waiting for Attachment...")
        
        try:
            ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch)
            raise EndProgramSignal("Program Terminated: Open Failed")

        print("--------------------\n"
            "\n  | The output of a DigitalOutput channel can be controlled by setting its Duty Cycle.\n"
            "  | The Duty Cycle can be a number from 0.0 or 1.0\n"
            "  | Some devices only accept Duty Cycles of 0 and 1.\n"
            "\nInput a desired duty cycle from 0.0 or 1.0 and press ENTER\n"
            "Input Q and press ENTER to quit\n")

        end = False
        state = False

        while (end != True):
            buf = sys.stdin.readline(100)
            if not buf:
                continue

            if (buf[0] == 'Q' or buf[0] ==  'q'):
                end = True
                continue
            
            try:
                dutyCycle = float(buf)
            except ValueError as e:
                print("Input must be a number, or Q to quit.")
                continue

            if (dutyCycle > 1.0 or dutyCycle < 0.0):
                print("Duty Cycle must be between 0.0 and 1.0")
                continue

            print("Setting DigitalOutput DutyCycle to " + str(dutyCycle))
            ch.setDutyCycle(dutyCycle)

        print("Cleaning up...")
        ch.close()
        print("\nExiting...")
        return 0

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        traceback.print_exc()
        print("Cleaning up...")
        ch.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        ch.close()
        return 1
    except RuntimeError as e:
         sys.stderr.write("Runtime Error: \n\t" + e)
         traceback.print_exc()
         return 1
    finally:
        print("Press ENTER to end program.")
        readin = sys.stdin.readline()

main()

