import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json

#Provide your IBM Watson Device Credentials
organization = "3enokg"
deviceType = "iotdevice"
deviceId = "1001"
authMethod = "token"
authToken = "1234567890"


# Initialize the device client.
T=0
H=0

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])
        m=cmd.data['command'] 

        if m=='onlight':
                print("LIGHT ON IS RECEIVED")
                
                
        elif m=='offlight':
                print("LIGHT OFF IS RECEIVED")
        elif m=='offfan':
                print("FAN OFF IS RECEIVED")
        elif m=='onfan':
                print("FAN ON IS RECEIVED")
        elif m=='offAC':
                print("AC OFF IS RECEIVED")
        elif m=='onAC':
                print("LIGHT OFF IS RECEIVED")
        """elif m=='offfridge':
                print("LIGHT OFF IS RECEIVED")
        elif m=='onfridge':
                print("LIGHT OFF IS RECEIVED")
        elif m=='close the door':
                print("LIGHT OFF IS RECEIVED")
        elif cm=='open the door':
                print("LIGHT OFF IS RECEIVED")"""
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        T=23
        H=45
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'temperature' : T, 'humidity': H }}
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % T, "Humidity = %s %%" % H, "to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
