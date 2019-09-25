import RPi.GPIO as GPIO #import the GPIO library
import sys, subprocess, time, threading
from picamera import PiCamera #Pi Camera Library
from time import sleep, time
import io, json, subprocess, base64
from PIL import Image #Pillow library to convert photo to memory buffer
import requests    #To make api call

pinNumber=6

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
   
        if(GPIO.input(pinNumber) == 1):
            print("1")
            #time.sleep(2)

        else:
            
            print("---- Starting Camera -----")
            photo_taken_time = int(time())
            stream = io.BytesIO() # Set up a stream object for the photo taken

            ### Taking photos
            with PiCamera() as camera:
                camera.resolution = (800, 600)
                camera.start_preview(fullscreen=False, window=(100, 20, 640, 480))
                sleep(2)
                camera.capture(stream, format='jpeg', resize=(640, 480)) #Buffered image stream wihch will be sent to API GW on-the-fly

            stream.seek(0) #Before this sys call, the stream is at the end of its position, which means if we don't call the stream to go back to its first position(0 posibtion), the data will actually will none/null(0)


            # Jason's API url_compare_faces = 'https://6fc23h655b.execute-api.ap-southeast-2.amazonaws.com/dev' # This is the api call to facerekgonition lambda function
            url_compare_faces = 'https://mwm1tvyyb0.execute-api.ap-northeast-1.amazonaws.com/dev'
            res = requests.post(url = url_compare_faces,
                                data = stream,
                                headers = {'Content-Type': 'application/octet-stream'}) #Make sure the API has settings to accept binary data

            stream.seek(0)

            res_json = json.loads(res.text)
            print(type(res_json))

            
                    
                    
                    
        
        
        #time.sleep(1)


