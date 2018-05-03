import RPi.GPIO as GPIO

#Pin Belegung
tasterPin1 = 11
tasterPin2 = 13
tasterPin3 = 15

#Board Modus (Alternativ GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

#Pin Setup als Eingaenge
GPIO.setup(tasterPin1, GPIO.IN)
GPIO.setup(tasterPin2, GPIO.IN)
GPIO.setup(tasterPin3, GPIO.IN)

value = GPIO.input(tasterPin1)
oldValue = 0
counter = 0

def call1(tasterPin1):
    global counter
    counter = counter +1
    print (counter)

def call2(tasterPin2):
    global counter
    counter = counter -1
    print (counter)
    
def call3(tasterPin3):
    global counter
    counter = 0
    print (counter)

GPIO.add_event_detect(tasterPin1, GPIO.FALLING, callback = call1, bouncetime = 200)   
GPIO.add_event_detect(tasterPin2, GPIO.FALLING, callback = call2, bouncetime = 200)
GPIO.add_event_detect(tasterPin3, GPIO.FALLING, callback = call3, bouncetime = 200)  

try:
    while True:
     x = 0  
             
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print ("Programm Beendet")
