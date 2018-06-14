# Kiosk System

###### Hochschule München - Projekt Technische Informatik Nr. 6 - SS18

## Einleitung

Der sogenannte Kiosk-Modus eines Betriebssystems zeichnet sich durch eingeschränkte Rechte für den Benutzer aus, um ausschließlich gewünschte Inhalte zu zeigen. 
Möchte man eine Python Applikation für einen Raspberry Pi mit Raspbian programmieren, die Webinhalte oder lokale HTML Dateien in einem Kiosk Modus anzeigt und per Hardware-Taster kontrollierbar macht, ist folgendes Vorgehen möglich.

### Wahl der graphischen Benutzeroberfläche

Python bietet einige GUI Pakete wie *TKinter*, *PySide* oder *PyQT*. Da sich die Umsetzung einer Web-Ansicht mit dem Python Standard *TKinter* allerdings nur schwierig umsetzen lässt, ist *PyQt5* besser geeignet. Zudem ist *Qt* ist ein plattformübergreifender Standard für die Entwicklung von graphischen Benutzeroberflächen und für den Raspberry Pi bestens geeignet. Die Evaluierung anderer Pakete wurde deshalb nicht mehr in Betracht gezogen.

### GPIO Ports verwenden

Der Raspberry Pi besitzt einige General Purpose Input Output (GPIO) Ports, deren Status mithilfe der Python GPIO Methoden ausgelesen werden kann. Die Hardware Komponenten sind daher an diese Ports angeschlossen.

### Taster

Im Kiosk Projekt kommen 3 Taster zum Einsatz. Hiervon ist ein Taster Teil des Drehgebers, der aber genauso angesprochen wird wie die restlichen beiden Taster. Die Taster sind jeweils mit externen 10 kOhm Pull-Up Widerständen verbunden (Invertierte Logik). Details befinden sich in der Code Dokumentation.

### Drehgeber

Bei der Drehung um einen Einrastpunkt emittiert ein typischer Drehgeber auf seinen 2 Ausgangspins einen 2 Bit Gray Code. Jeder Schritt, der meistens durch einen physikalischen Klick begleitet wird, generiert dabei eine Sequenz an 5 Output Codes.

Position  | Bit1 | Bit2
--------- | ---- | ------
Start 		| 0		| 0
1/4  		| 1		| 0
1/2			| 1		| 1
3/4			| 0		| 1
Ende		| 0 	| 0

Die Richtung der Drehbewegung wird durch den Ablauf der Codetabelle festgelegt. Entweder wird sie von oben nach unten, oder umgekehrt durchlaufen.

Über eine State Machine wird der richtige Durchlauf der Codefolgen nachverfolgt. Vorteil dieser Methode ist unter anderem Störfestigkeit (Bei einem eigentlich nicht möglichen Übergang der Pins von 10 auf 01 wird zum Beispiel die State Machine wieder auf 00 resettet). Außerdem ist der Drehgeber hierdurch entprellt, ohne zusätzliche Entprell-Kondensatoren oder Software Algorithmen zu benötigen.

Die 2 Bit Pins des Drehgebers sind jeweils mit 10 kOhm Pull-Up Widerständen auf Vcc (3.3V am Raspberry) verbunden.


### Threading und Signals

Sobald eine Python Applikation mit ``app-exec_`` gestartet wurde, werden keine weiteren Methodenaufrufe mehr zugelassen. Damit die GUI Applikation und die GPIO Funktion also gleichzeitig ablaufen und kommunizieren muss mit ``Threading`` gearbeitet werden. Die Übertragung zwischen den Threads erfolgt über sogenannte ``Signals``. 

## Code Dokumentation

### Pakete importieren

**GUI Pakete**

```
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKit import QWebSettings
```

Die Unterpakete von PyQt5 werden später erläutert.

**Interaktion mit dem File-System**

```
import os

```

``os`` dient unter anderem zur Pfadmanipulation mittels ``os.path`` oder zur Pfaditeration mittels ``os.walk``.

**Python Interpreter**

```
import sys
```

**Zeit Funktionen**

Beispielsweise zum endlosen Warten.

```
import time
```

Mit ``sys.argv[1]`` lässt sich beispielsweise der erste Parameter beim Aufruf über die Kommandozeile angeben. Das ``sys`` Modul stellt also Informationen über den Python-Interpreter zur Verfügung.

**GPIO**

```
import RPi.GPIO as GPIO

```

**Threading und Signals**

```
from PyQt5.QtCore import QThread, pyqtSignal

```

Die Applikation muss im *Main Thread* laufen (d.h. nicht in einem eigenem Thread) und von dort aus können parallel beliebig viele weitere Threads gestartet werden, sofern sie als ``QThread`` initialisiert worden sind. Über ``signals`` können die Threads dann miteinander und mit dem *Main Thread* kommunizieren. 

### Globale Variablen definieren

```
fileList = list()
fileCounter = 0

```

``fileList`` wird als leere Liste initialisiert um später die Namen der anzuzeigenden HTML-Dateien zu speichern. 

Der ``fileCounter`` wird mit 0 initialisiert und später erhöht oder erniedrigt, je nachdem ob die vorherige oder die nächste Seite ausgewählt wird. Der Zahlenbereich wird durch die Länge von ``fileList``bestimmt.

### Methoden

**Das Verzeichnis mit den (HTML) Dateien auslesen**

```
def setDir():
    if len(sys.argv) is 1:
    	print("Please specify HTML directory as first argument")
    	sys.exit()
    directory = os.path.join(os.path.abspath(sys.argv[1]), '')
    return directory

```

Das Verzeichnis kann als erstes Argument in der Kommandozeile angegeben werden. In der Variablen ``directory`` wird der Pfad zu den HTML Dateien gespeichert. ``join`` erzeugt aus allen übergebenen Parametern einen ``/``separierten Pfad. In diesem Fall werden der Pfad und ein Leerstring zusammengefügt, was nichts anderes bedeutet, als ein ``/``anzuhängen. 

**Eine Datei öffnen** 

```
def openFile(file):
    dir = setDir()
    path = os.path.join(dir, file)
    try:
       with open(path) as f:
            data = f.read()
       return data
    except OSError as e:
        if e.errno == errno.ENOENT:
            print(e)
        else:
            raise          
```

Dabei wird die erstellte ``setDir`` Methode zum Auslesen des Verzeichnisses verwendet, der übergebene Dateiname ``file``geöffnet und die Datei mit ``read`` ausgelesen. Im Fehlerfall wird eine Exception geschmissen (vergleichbar zur anderen Programmiersprachen). Wenn der Fehler ein ``File not found`` Fehler ist, wird dieser ausgegeben. Ansonsten wird der Zähler für die Fehlerart erhöht. Jeder Fehler ist einer Nummer zugeordnet (z.B. ``ENOENT = 2``).

**Die Liste mit den Dateien füllen** 

```
def initFileList():
    directory = setDir()
    fileSet = set() 
    for root, dirs, files in os.walk(directory): 
        for fileName in files:
            if fileName.endswith('.html'):
                fileSet.add(os.path.join(root[len(directory):], fileName))
    fileList = list(fileSet) 
    fileList.sort()
    return fileList
```

Hier wird wieder die ``setDir``Methode verwendet um den angegebenen Pfad zu erhalten. Danach wird eine Liste als ``set`` initialisiert, welches keine doppelten Elemente enthalten kann. Falls diese Eigenschaft nicht gewünscht ist, kann mit ``list.append()``gearbeitet werden. 

 Alle Dateinamen mit der spezifizierten Endung werden dem ``set`` hinzugefügt und anschließend wieder in eine Liste umgewandelt und zurückgegeben. Da ein ``set`` nicht sortiert ist, wird das mit ``sort``noch erledigt. 


### Klassen

Der Python Code enthält eine Klasse für die graphische Oberfläche und eine für die GPIO Funktion. 

#### GUI 

Die Klasse wird als ``QWebView`` initialisiert. Diese ist mit Methoden ausgestattet, welche unter anderem Webinhalte und lokale HTML Dateien anzeigen können.

```
class Infoscreen(QWebView):      
```

Es folgen nun sieben interne Funktionen:

Zuerst die sich rekursiv aufrufende Initialisierungsfunktion.

```
def __init__(self):
    super(Infoscreen, self).__init__()
    self.setWindowTitle('Infoscreen')
    self.titleChanged.connect(self.adjustTitle)
``` 
 
Nach dem Aufruf von ``__init__`` können Einstellungen für das Fenster vorgenommen werden. In diesem Fall wird nur der Titel bearbeitet. 

``` 
def adjustTitle(self):
    self.setWindowTitle(self.title())

def disableJS(self):
    settings = QWebSettings.globalSettings()
    settings.setAttribute(QWebSettings.JavascriptEnabled, False)
```

``adjustTitle`` setzt den Titel der Anwendung und ``disableJS`` bietet die Möglichkeit JavaScript Funktionen ein -oder auszuschalten. Mit den Methoden der ``QWebSettings`` können die Einstellungen gespeichert werden, welche dann von der ``QWebView`` genutzt werden. 

```
def keyPressEvent(self, event):
    if event.key() == Qt.Key_Escape:
        self.close()
```

In ``keyPressEvent`` kann eine Taste oder Tastenkombination angegeben werden, um die Anwendung zu schließen und aus dem Vollbildmodus zurückzukehren. Das ist in der Entwicklungsphase und später für den Administrator sehr hilfreich.

```
def switchPage(self, fileIndex):
    fileList = initFileList()
    try:
        file = fileList[fileIndex]
        html = openFile(file)
        self.setHtml(html,QUrl.fromLocalFile(setDir()))
    except IndexError as e:
        print(e)
```

Die Methode ``switchPage`` nutzt alle erstellten globalen Methoden zur Anzeige der nächsten oder vorherigen HTML Seite. Der Parameter ``fileIndex`` bestimmt, welche der in ``fileList`` enthaltenen Dateien ausgewählt werden soll. Danach wird diese Datei geöffnet und mithilfe der ``QWebView``- Funktion ``setHTML`` in die Oberfläche geladen. Entscheidend ist dabei die Verwendung von ``QUrl`` zur Unterscheidung von lokalen und gehosteten Quelldateien. Falls der übergebene Index größer als die Länge der Dateiliste ist, wird ein ``IndexError``geschmissen. Da dieser allerdings von der Liste abhängt, kann das im Normalfall nicht passieren.


```
def update(self, action):
    global fileCounter
    fileIndex = len(initFileList())
    if action == "fwd":
        if fileCounter<fileIndex-1:
            fileCounter = fileCounter + 1
        else:
            fileCounter = 0
        self.switchPage(fileCounter)
    elif action == "bwd":
        if fileCounter>0:
            fileCounter = fileCounter -1
        else:
            fileCounter = fileIndex-1
        self.switchPage(fileCounter)
    elif action == "home":
        fileCounter = 0
        self.switchPage(fileCounter)
    elif action == "up":
        self.page().mainFrame().scroll(0,-100)
    elif action == "down":
        self.page().mainFrame().scroll(0,100)
    else:
        pass
```

Hier wird der globale ``fileCounter`` je nach Signal erhöht oder erniedrigt und die nächste oder vorherige Seite mit ``switchPage`` angezeigt. Außerdem sind zwei Events für die Scroll-Funktion und eines für die Rückkehr zu ersten Seite ``home`` angelegt. Der Zähler hängt von der Länge der Dateiliste ab und ist durch diese begrenzt. Wenn die letzte Datei erreicht wurde, wird wieder die erste angezeigt (und anders herum).

```
def connect_input(self, inputthread):
    inputthread.update_signal.connect(self.update)
```

Die letzte interne Methode dient zur Verbindung der Threads mit der GUI Klasse. Die Methode wird beim Start der Anwendung jeweils einmal für alle vorhandenen Threads (in diesem Fall nur der GPIO Thread) aufgerufen. Der Übergabeparameter ist die Thread Klasse, sofern sie als ``QThread`` initialisiert worden ist.

### GPIO

Die zweite Klasse reagiert auf Änderungen an den GPIO Pins. Sie wird, wie angesprochen, als ``QThread`` angelegt:

```
class GPIO_Thread(QThread):
```

Als nächstes wird eine Signalvariable erstellt, die das ``pygtSignals`` Paket nutzt, um eine Verbindung mit der ``update`` Methode der GUI-Klasse herzustellen.


```
update_signal = pyqtSignal(str, name='update')
```

Bei der Initialisierung wird die Methode wieder rekursiv aufgerufen und der Thread-Zustand mit 0 vorbelegt:

```
def __init__(self):
        super(GPIO_Thread, self).__init__()
        self.state = 0
```

Danach wird die ``QThread`` Methode ``run`` überschrieben und der gesamte *GPIO* Code dort platziert.

```
def run(self):
```

<u>Schritt 1</u>: Integer-Variablen für die Taster und den Drehgeber definieren:

```
tasterPin1 = 11
tasterPin2 = 13
tasterPin3 = 15  
drehgeberPin1 = 16
drehgeberPin2 = 18
```

Die Zahlen entsprechen den Nummern der Raspberry Pins, welche als GPIO Pins konfiguriert sind. Die Belegung ist nochmals in den folgenden Tabellen zusammengefasst:

**Taster Pinbelegung**

Taster |	Pin    |	GPIO
------ | ------- | -------
Taster1 | 11	    | 17
Taster2 | 13     | 27
Taster3 (Drehgeber) | 15 | 22

**Drehgeber Pinbelegung**

Drehgeber |	Pin    |	GPIO
------ | ------- | -------
Pin1 (Bit1) | 16 | 23
Pin3 (Bit2) | 18 | 24

**VCC/GND**

-|	Pin    
------ | ------- 
VCC (3.3V) | 17
GND | 9  

$\:$
<u>Schritt 2</u>: GPIO Board Modus setzen. 

```
GPIO.setmode(GPIO.BOARD)
```

Das bedeutet, dass die Pin Nummern auf der Raspberry Pi Platine verwenden werden. Eine Alternative sind die GPIO-Pins mittels ``GPIO.BCM``, welche sich allerdings in den Versionen des Raspberry Pi unterscheiden können und somit keine Eindeutigkeit gegeben ist.

<u>Schritt 3</u>: Eingänge definieren.

```
GPIO.setup(tasterPin1, GPIO.IN)
    GPIO.setup(tasterPin2, GPIO.IN)
    GPIO.setup(tasterPin3, GPIO.IN)
    GPIO.setup(drehgeberPin1, GPIO.IN)
    GPIO.setup(drehgeberPin2, GPIO.IN)
```

<u>Schritt 4</u>: Konstanten für den Drehgeber festlegen.

```
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
```

Die ersten drei Konstanten repräsentieren eine Links-, eine Rechts- oder keine Drehung. Die restlichen Konstanten sind die Zustände der Zustandsmaschine, welche im einführenden Kapitel erläutert wurde. 

<u>Schritt 5</u>: Die Zustandstabelle anlegen:

```
ttable = [[R_START, R_CW_BEGIN, R_CCW_BEGIN, R_START],
         [R_CW_NEXT, R_START, R_CW_FINAL, R_START|DIR_CW],
         [R_CW_NEXT, R_CW_BEGIN, R_START, R_START],
         [R_CW_NEXT, R_CW_BEGIN, R_CW_FINAL, R_START],
         [R_CCW_NEXT, R_START, R_CCW_BEGIN, R_START],
         [R_CCW_NEXT, R_CCW_FINAL, R_START, R_START|DIR_CCW],
         [R_CCW_NEXT, R_CCW_FINAL, R_CCW_BEGIN, R_START]]

```

<u>Schritt 6</u>: Den Status vorinitialisieren:

```
self.state = R_START
```

<u>Schritt 7</u>: Den drei Tastern und dem Drehgeber eine Event Methode zuordnen (Taster 2 und 3 analog):

```
def call1(channel):
    self.update_signal.emit("fwd")           
```

Der Übergabeparameter ist der zugehörige Kanal und mithilfe der ``emit`` Methode wird ein Signal gesendet. 

Zum Vergleich: In der GUI-Klasse wurde ebenfalls eine Methode mit ``update_signal`` erstellt - dort aber eine ``connect`` Funktion aufgerufen um die graphische Oberfläche als Empfänger festzulegen. 

Beim Drehgeber muss vor dem senden noch ermittelt werden, welche Aktion genau ausgeführt wurde. Dazu wird in ``pinstate`` zunächst die aktuelle Pin Nummer gespeichert, der passende Wert in der Matrix gesucht und auf ``DR_CW`` oder ``DIR_CCW`` geprüft. 

```
def call4(channel):
    pinstate = ((GPIO.input(drehgeberPin2) << 1)| GPIO.input(drehgeberPin1))
    self.state = ttable[self.state & 0xf][pinstate]
    if self.state ==  DIR_CW:
        self.update_signal.emit("down")
    elif self.state == DIR_CCW:
        self.update_signal.emit("up")
```

Wird ein Taster gedrückt, löst dieser bei einer fallenden Flanke einen Interrupt aus, und springt in eine der oben erwähnten Callback Funktionen, in der weitere Funktionalität ausgeführt wird. Jeder Taster hat hierbei eine eigene Callback Funktion.

Mittels der GPIO.RPI Library wird ebenfalls ein softwareseitiges Entprellen (bouncetime = 200ms) eingeschaltet (Die anderen Taster analog).

```  
GPIO.add_event_detect(tasterPin1, GPIO.FALLING, callback = call1function, bouncetime = 200)
```

Für den Drehgeber sieht das ähnlich aus - nur ohne Bouncetime (Drehgeber Pin 2 analog):

```
GPIO.add_event_detect(drehgeberPin1, GPIO.BOTH, callback = call4)
```

Informationen können mit den Callback Funktionen nur durch globale Variablen weitergereicht werden.

<u>Schritt 8</u>: Mit einer Endlosschleife dafür sorgen, dass die ``run`` Methode während der Laufzeit nicht verlassen wird:

```
while True:
     time.sleep(1)
```

Nach der ``run`` Methode folgt noch eine "Aufräum" -Funktion:

```
   def __del__(self):
        GPIO.cleanup()
```

Zum Schluss muss die Applikation noch gestartet werden (Als ``QApplication`` initialisiert).

```
def main():
    app = QApplication(sys.argv)
    screen = Infoscreen()
    screen.switchPage(0)
    screen.showFullScreen()
    inputthread = GPIO_Thread()
    inputthread.start()
    screen.connect_input(inputthread)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

Weiter wird die GUI Klasse ``Infoscreen`` aufgerufen und die erste HTML Seite mit ``switchPage`` geladen. Danach wird der Vollbildmodus aktiviert und der GPIO Thread gestartet. Wenn die GPIO Instanz existiert, kann die oben erwähnte ``connect_input`` Methode für den Thread aufgerufen werden. 

Als letztes geschieht der ``main``Aufruf und der Infoscreen startet.