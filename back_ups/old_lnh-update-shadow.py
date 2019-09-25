from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json
import time
import logging
from datetime import datetime
import threading
import time
import RPi.GPIO as GPIO #import the GPIO library
import time

pinNumber=5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#import dns.resolver #import the module
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.ERROR)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
JSONPayload =""
def callback(client, userdata, message):
     logging.info(userdata)

# init data 

thingName = "always-test-iot"
myAWSIoTMQTTShadowClient = None

stopThread = False
def thread_function(epochTime):
    while True:
       logging.info("Thread %s: starting", epochTime)
       time.sleep(1)
       if stopThread :
            break
       if (int(time.time() - epochTime)/60) >=1 :
           tempMQTTConnection = myAWSIoTMQTTShadowClient.getMQTTConnection()
           #JSONPayload = {"deviceStatus":"DoorOpened","deviceID":"always-test-iot"}
           JSONPayload = '{"errorType":"DoorKeepOpen","deviceID":"'+thingName+'"}'
           tempMQTTConnection.publish("LNH_ALARM",JSONPayload,1)
           break

       logging.info("Thread %s: continue", epochTime)


def updateDoorStatusShadow(doorStatus): 
      global stopThread
      JSONPayload = '{"state":{"reported":{"recordType": "Door", "deviceID":"'+thingName+'","doorStatus":"'+doorStatus +'"}}}'
      deviceShadowHandler.shadowUpdate(JSONPayload, callback, 5)
      if(doorStatus == "CLOSE"):
          stopThread = True
          #updateAuthenticationShadow("NO","N/A")
      else:
         stopThread = False
         x = threading.Thread(target=thread_function, args=(int(time.time()),))
         x.start()
def updateAuthenticationShadow(status,name):
      JSONPayload = '{"state":{"reported":{"recordType": "Authentication","authenticationStatus":"'+status+'","userName":"'+name+'"}}}'
     # print(JSONPayload)
      deviceShadowHandler.shadowUpdate(JSONPayload, callback, 5)    
#connect to AWS

myAWSIoTMQTTShadowClient = None

#lastWillPayload = {"errorType":"Device"}
lastWillPayload = '{"errorType":"Device","deviceID":"'+thingName+'"}'

myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(thingName)
myAWSIoTMQTTShadowClient.configureEndpoint("a1f18ishzwlosz-ats.iot.ap-southeast-2.amazonaws.com", 8883)
#myAWSIoTMQTTShadowClient.configureCredentials("./AmazonRootCA1.pem", "./f45483b5db-private.pem.key", "./f45483b5db-certificate.pem.crt")
myAWSIoTMQTTShadowClient.configureCredentials("./AmazonRootCA1.pem", "./90b9981671-private.pem.key","./90b9981671-certificate.pem.crt")
myAWSIoTMQTTShadowClient.configureLastWill("LNH_ALARM", lastWillPayload, 1)

#myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
#myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
#myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

connected = myAWSIoTMQTTShadowClient.connect(keepAliveIntervalSecond=30)
print("Connection : "+str(connected))
#MQTTClient = myAWSIoTMQTTShadowClient.getMQTTConnection()
#MQTTClient.configureOfflinePublishQueueing(10,0)
# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
#print("preparing to get shadow")

# Update shadow in a loop
#deviceShadowHandler.shadowGet(callback,5)
#print(JSONPayload)
#deviceShadowHandler.shadowDelete(callback,5)
#time.sleep(10)
#deviceShadowHandler.shadowGet(callback,5)
#time.sleep(10)
loopCount = 0
#updateDoorStatusShadow("OPEN")
previous_status = 0
updateDoorStatusShadow("OPEN")
while True:
    print(GPIO.input(pinNumber))
    if (previous_status != GPIO.input(pinNumber)):
        if(GPIO.input(pinNumber) == 1):
            print("I am sending message door is open")
            updateDoorStatusShadow("OPEN")
        else:
            print("I am sending message door is closed")
            updateDoorStatusShadow("CLOSE") 
        previous_status = GPIO.input(pinNumber)

    time.sleep(1)


#print("alarm should be sent")
#time.sleep(100)

#myAWSIoTMQTTShadowClient.disconnect()
#time.sleep(60)
# while True:
#     print("I am in the loop")
#     JSONPayload = '{"state":{"reported":{"test":"true","doorStatus":"Open","abcdef":{"abc": "true", "cdef": "time"},"timestamp":'+str(int(time.time()))+ '}}}'
#     print(JSONPayload)
#     deviceShadowHandler.shadowUpdate(JSONPayload, callback, 5)
#     loopCount += 1
#     #print(JSONPayload)
#     time.sleep(60)
#     JSONPayload = '{"state":{"reported":{"authentication":"Yes","timestamp":'+str(int(time.time()))+ '}}}'
#     deviceShadowHandler.shadowUpdate(JSONPayload, callback, 5)
#     time.sleep(5)
#     JSONPayload = '{"state":{"reported":{"doorStatus":"Close","timestamp":'+str(int(time.time()))+ '}}}'
#     deviceShadowHandler.shadowUpdate(JSONPayload, callback, 5)
#     print("------- END -------")
#     time.sleep(60)

    
