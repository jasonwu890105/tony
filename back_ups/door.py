import RPi.GPIO as GPIO #import the GPIO library
import time

pinNumber=5

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP)

name = "Ryan"
print("Hello " + name)

while True:
    print(GPIO.input(pinNumber))
    time.sleep(1.5)
    #if GPIO.input(27):
     #  print("Door is open")
     #  time.sleep(2)
    #if GPIO.input(27) == False:
     #  print("Door is closed")
      # time.sleep(2)