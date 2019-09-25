from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import threading
import RPi.GPIO as GPIO #import the GPIO library
from datetime import datetime

###########
# Config
###########

thingName = "door1"
awsEndpoint = "a1i6g0p2oq1mjn-ats.iot.ap-northeast-1.amazonaws.com"
awsPortNumber = 8883
awsRootCAPath = "./AmazonRootCA1.pem"
awsIoTPrivateKeyPath = "./Elliots_certs/e0947a73d2-private.pem.key"
awsIoTCertificatePath = "./Elliots_certs/e0947a73d2-certificate.pem.crt"
awsTopicPrefix = "SYD37/"


###################
# Sensor Pin config
###################
pinNumber=5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)
myAWSIoTMQTTClient = None


#############################
# Left Open Alarm
############################
stopThread = False
def thread_function(epochTime):
    while True:
       time.sleep(1)
       if stopThread :
            break
       if (int(time.time() - epochTime)/30) >=1 :
           JSONPayload = '{"recordType":"Alarm","errorType":"DoorKeepOpen"}'
           myAWSIoTMQTTClient.publish(awsTopicPrefix + thingName,JSONPayload,0)
           break


############################
# Updating Door status
###########################
def updateDoorStatus(doorStatus):
    global stopThread
    JSONPayload = '{"recordType": "Door","doorStatus":"'+doorStatus +'"}'
    myAWSIoTMQTTClient.publish(awsTopicPrefix + thingName,JSONPayload,1)

    # DoorKeptOpen Alarm
    if (doorStatus == "CLOSED"):
        stopThread = True
    elif (doorStatus == "OPEN") :
        stopThread = False
        x = threading.Thread(target=thread_function, args=(int(time.time()),))
        x.start()

###############################################
# Update Device Status Connected / Disconnecred
###############################################
def updateDeviceStatus(deviceStatus):
      JSONPayload = '{"recordType": "Device","deviceStatus":"'+deviceStatus +'"}'
      myAWSIoTMQTTClient.publish(awsTopicPrefix + thingName,JSONPayload,1)



########################################



#======================================
# AWS IoT SDK - MQTT Client connection
#======================================
myAWSIoTMQTTClient = AWSIoTMQTTClient(thingName)
myAWSIoTMQTTClient.configureEndpoint(awsEndpoint, awsPortNumber)
myAWSIoTMQTTClient.configureCredentials(awsRootCAPath, awsIoTPrivateKeyPath,awsIoTCertificatePath)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

# Last will payload for disconnection
lastWillPayload = '{"recordType":"Device","deviceStatus":"Disconnected"}'
myAWSIoTMQTTClient.configureLastWill(awsTopicPrefix + thingName, lastWillPayload, 0)


# Connect

myAWSIoTMQTTClient.connect()
updateDeviceStatus("Connected")
dateTimeObj = datetime.now()
print("Device is connected at "+ str(datetime.now()))

previous_status = 2

# Listen to door sensor and publish

while True:
    if (previous_status != GPIO.input(pinNumber)):
        if(GPIO.input(pinNumber) == 1):
            print("Door is opened at "+ str(datetime.now()))
            updateDoorStatus("OPEN")
        else:
            print("Door is closed at "+ str(datetime.now()))
            updateDoorStatus("CLOSED")
        previous_status = GPIO.input(pinNumber)
    time.sleep(1)

