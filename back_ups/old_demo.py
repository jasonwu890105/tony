from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json
import time
import logging
from datetime import datetime
import threading
import time
import RPi.GPIO as GPIO #import the GPIO library

pinNumber=5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#connect to AWS
thingName = "always-test-iot"
myAWSIoTMQTTClient = None

stopThread = False
def thread_function(epochTime):
    while True:
       logging.info("Thread %s: starting", epochTime)
       time.sleep(1)
       if stopThread :
            break
       if (int(time.time() - epochTime)/60) >=1 :
           
           #JSONPayload = {"deviceStatus":"DoorOpened","deviceID":"always-test-iot"}
           JSONPayload = '{"errorType":"DoorKeepOpen","deviceID":"'+thingName+'"}'
           myAWSIoTMQTTClient.publish("LNH_ALARM",JSONPayload,1)
           break

       logging.info("Thread %s: continue", epochTime)

def updateDoorStatus(doorStatus): 
      global stopThread
      JSONPayload = '{"recordType": "Door","doorStatus":"'+doorStatus +'"}'
      myAWSIoTMQTTClient.publish("LNH_STATUS/"+thingName,JSONPayload,1)
      if(doorStatus == "CLOSE"):
          stopThread = True
      else:
         stopThread = False
         x = threading.Thread(target=thread_function, args=(int(time.time()),))
         x.start()

myAWSIoTMQTTClient = AWSIoTMQTTClient(thingName,cleanSession= False)
myAWSIoTMQTTClient.configureEndpoint("a1f18ishzwlosz-ats.iot.ap-southeast-2.amazonaws.com", 8883)

myAWSIoTMQTTClient.configureCredentials("./AmazonRootCA1.pem", "./90b9981671-private.pem.key","./90b9981671-certificate.pem.crt")
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)
lastWillPayload = '{"errorType":"Device","deviceID":"'+thingName+'"}'
myAWSIoTMQTTClient.configureLastWill("LNH_ALARM", lastWillPayload, 0)


myAWSIoTMQTTClient.connect()

previous_status = 2
while True:
    print(GPIO.input(pinNumber))
    if (previous_status != GPIO.input(pinNumber)):
        if(GPIO.input(pinNumber) == 1):
            print("I am sending message door is open")
            updateDoorStatus("OPEN")
        else:
            print("I am sending message door is closed")
            updateDoorStatus("CLOSE")
        previous_status = GPIO.input(pinNumber)

    time.sleep(1)









































































































































































































































