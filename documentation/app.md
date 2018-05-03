#Taster- und Drehgeber-Logik in Python

Kommandobefehle für Python und GPIO Updates

```
pi@raspberrypi ~ $ sudo apt-get update
pi@raspberrypi ~ $ sudo apt-get install python-dev
pi@raspberrypi ~ $ sudo apt-get install python-rpi.gpio
```
Taster Pinbelegung:

Taster |	Pin    |	GPIO
------ | ------- | -------
Taster1 | 11	    | 17
Taster2 | 13     | 27
Taster3 (Drehgeber) | 15 | 22

Drehgeber Pinbelegung:

Drehgeber |	Pin    |	GPIO
------ | ------- | -------
Pin1 (Bit1) | 16 | 23
Pin3 (Bit2) | 18 | 24

VCC/GND:

-|	Pin    
------ | ------- 
VCC (3.3V) | 17
GND | 9 

##Taster

Im Kiosk Projekt kommen 3 Taster zum Einsatz. Hiervon ist 1 Taster Teil des Drehgebers, dieser wird aber genauso angesprochen wie die restlichen 2 Taster. Die Taster sind jeweils mit externen 10 kOhm Pull-Up Widerständen verbunden (Invertierte Logik).

Wird ein Taster gedrückt, löst dieser bei einer fallenden Flanke einen Interrupt aus, und springt in eine Callback Funktion, in der weitere Funktionalität ausgeführt wird. Jeder Taster hat hierbei eine eigene Callback Funktion.
Mittels der GPIO.RPI Library wird ebenfalls ein softwareseitiges Entrepllen (bouncetime = 200ms) eingeschaltet.

```
def call1function(tasterPin1):
    global counter
    counter = counter +1
    print (counter)
    
GPIO.add_event_detect(tasterPin1, GPIO.FALLING, callback = call1function, bouncetime = 200)
```

Informationen können mit den Callback Funktionen nur durch globale Variablen weitergereicht werden.

##Drehgeber

Bei der Drehung um einen Einrastpunkt emittiert ein typischer Drehgeber auf seinen 2 Ausgangspins einen 2 Bit Gray Code. Jeder Schritt, der meistens durch einen physikalischen Klick begleitet wird, generiert dabei eine Sequenz an 5 Output Codes.

Position  | Bit1 | Bit2
--------- | ---- | ------
Start 		| 0		| 0
1/4  		| 1		| 0
1/2			| 1		| 1
3/4			| 0		| 1
Ende		| 0 	| 0

Die Richtung der Drehbewegung wird durch den Ablauf der Codetabelle festgelegt. Entweder wird sie von oben nach unten, oder umgekehrt durchlaufen.

Über eine State Machine wird der richtige durchlauf der Codefolgen nachverfolgt. Vorteil dieser Methode ist unter anderem Störfestigkeit (Bei einem eigentlich nicht möglichen Übergang der Pins von 10 auf 01 zum Beispiel wird die State Machine wieder auf 00 resettet) außerdem ist der Drehgeber hierdurch entprellt, ohne zusätzliche Entprell Kondensatoren oder Software Algorithmen zu benötigen.

Logik der Statemachine:

```
pinstate = ((GPIO.input(drehgeberPin2) << 1)| GPIO.input(drehgeberPin1))
        state = ttable[state & 0xf][pinstate]
```
Die Gray Code Tabelle befindet sich in einer 7x4 Matrix (ttable)

Die 2 Bit Pins des Drehgebers sind jeweils mit 10 kOhm Pull-Up Widerständen auf Vcc (3.3V am Raspberry) verbunden.

##GPIO Layout für Raspberry Pi 3

![GPIO PIN LAYOUT](https://cdn-images-1.medium.com/max/1600/1*pcfeGQr_mUJrXDFDrdKMww.png)