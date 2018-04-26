import RPi.GPIO as GPIO

#Pin Belegung
drehgeberPin1 = 13
drehgeberPin2 = 15

#Board Modus (Alternativ GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

#Pin Setup als Eingaenge
GPIO.setup(drehgeberPin1, GPIO.IN)
GPIO.setup(drehgeberPin2, GPIO.IN)

try:
    #Konstanten
    DIR_NONE = 0x0
    DIR_CW = 0x10
    DIR_CCW = 0x20
    
    R_START = 0x0
    R_CW_FINAL = 0x1
    R_CW_BEGIN = 0x2
    R_CW_NEXT = 0x3
    R_CCW_BEGIN = 0x4
    R_CCW_FINAL = 0x5
    R_CCW_NEXT = 0x6
    
    #Full Table Deklaration
    ttable = [[R_START, R_CW_BEGIN, R_CCW_BEGIN, R_START],
             [R_CW_NEXT, R_START, R_CW_FINAL, R_START|DIR_CW],
             [R_CW_NEXT, R_CW_BEGIN, R_START, R_START], 
             [R_CW_NEXT, R_CW_BEGIN, R_CW_FINAL, R_START],
             [R_CCW_NEXT, R_START, R_CCW_BEGIN, R_START],
             [R_CCW_NEXT, R_CCW_FINAL, R_START, R_START|DIR_CCW],
             [R_CCW_NEXT, R_CCW_FINAL, R_CCW_BEGIN, R_START]]
    
    #State Vorinitialisieren
    state = R_START
    
    while True:
        pinstate = ((GPIO.input(drehgeberPin2) << 1)| GPIO.input(drehgeberPin1))
        state = ttable[state & 0xf][pinstate]
        
        if state ==  DIR_CW:
            print ("Rechts")
        elif state == DIR_CCW:
            print ("Links")
             
except KeyboardInterrupt:
    GPIO.cleanup()
    print ("Programm Beendet")