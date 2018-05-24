import PyQt5
import sys
import os.path
import os
import inspect
import RPi.GPIO as GPIO
import threading
import time
from PyQt5.QtCore import QUrl, QThread
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtWebKit import QWebSettings

##Global variables
##Counter for the button action
counter = 0
fileCounter = 0
i = 99

## Get the current working directory
def setDir():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    directory = os.path.dirname(os.path.abspath(filename))
    return directory

## Open the file in the path specified by <setDir()>
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

def initFileList():
     # Get the current working directory #       
    directory = setDir()

    fileSet = set() # Create a set to collect the files of <directory> #
    
    for root, dirs, files in os.walk(directory): # Add all file names to the set #
        for fileName in files:
            if fileName.endswith('.html'):
                fileSet.add(os.path.join(root[len(directory):], fileName))
    
    fileList = list(fileSet) # Create a list from the set to use the list functions
    fileList.sort()
##    print(fileList)# Sort the elements
    return fileList

## The GUI class 
class Infoscreen(QWebView):
    def _init_(self):
        self.view = QWebView._init_(self)
        #self.view = QWebView()
        self.setWindowTitle('Infoscreen')
        self.titleChanged.connect(self.adjustTitle)
        
        #directory = os.path.abspath(os.path.dirname(_file_))        
        #directory = os.path.join(os.getcwd())       
        #directory = os.path.abspath(os.path.dirname(sys.argv[0]))        
        #directory = abspath(getsourcefile(lambda:0))
        
    ## Set the html file into the screen
    def load(self,url):
        #self.setUrl(QUrl(url))
##        self.setHtml(url)
        self.setPage(QWebPage())
        
    def adjustTitle(self):
        self.setWindowTitle(self.title())
        
    def disableJS(self):
        settings = QWebSettings.globalSettings()
        settings.setAttribute(QWebSettings.JavascriptEnabled, False)
    
    ## Show the next html file
    def forward(self):
        global fileCounter
        fileList = initFileList()
        print(fileCounter)
        if fileCounter<8:
           fileCounter = fileCounter + 1
        else:
            fileCounter = 1
        try:
            file = fileList[fileCounter]
            html = openFile(file)
            self.load(html)
            print("Hallo")
        except IndexError as e:
            print(e)
          
    # Show the previous html file
    def back(self):
        global fileCounter
        fileList = initFileList()
        print(fileCounter)
        if fileCounter>1:
            fileCounter = fileCounter - 1
        else:
            fileCounter = 8
        try:
            file = fileList[fileCounter]
            html = openFile(file)
            self.load(html)
        except IndexError as e:
            print(e)

##class AThread(QThread):
##    def run(self):
##        print('Thread A')
####        app = QApplication(sys.argv)
##        view = Infoscreen()
##        view.showMaximized()
##        view.forward()
##        app.exec_()
        
class BThread(QThread):
    def run(self):
        print('Thread B')
        tasterPin1 = 11
        tasterPin2 = 13
        tasterPin3 = 15  #Taster vom Drehgeber
        drehgeberPin1 = 16
        drehgeberPin2 = 18

        #Board Modus (Alternativ GPIO.BCM)
        GPIO.setmode(GPIO.BOARD)

        #Pin Setup als Eingaenge
        GPIO.setup(tasterPin1, GPIO.IN)
        GPIO.setup(tasterPin2, GPIO.IN)
        GPIO.setup(tasterPin3, GPIO.IN)
        GPIO.setup(drehgeberPin1, GPIO.IN)
        GPIO.setup(drehgeberPin2, GPIO.IN)

        value = GPIO.input(tasterPin1)
        oldValue = 0
##        counter = 0

        def call1(tasterPin1):
##            global counter
##            counter = counter +1
##            print (counter)
            print(i)
            view = Infoscreen()
            view.forward()

        def call2(tasterPin2):
##            global counter
##            counter = counter -1
##            print (counter)
            view = Infoscreen()
            view.back()

        def call3(tasterPin3):
            global counter
            counter = 0
            print (counter)


        def call4(drehgeberPin1):
            GPIO.remove_event_detect(drehgeberPin1)
            GPIO.remove_event_detect(drehgeberPin2)
            state = R_START
            x = True
            while(x):
                pinstate = ((GPIO.input(drehgeberPin2) << 1)| GPIO.input(drehgeberPin1))
                state = ttable[state & 0xf][pinstate]

                if state ==  DIR_CW:
                    print ("Rechts")
                    x = False
                elif state == DIR_CCW:
                    print ("Links")
                    x = False
            GPIO.add_event_detect(drehgeberPin1, GPIO.BOTH, callback = call4)
            GPIO.add_event_detect(drehgeberPin2, GPIO.BOTH, callback = call5)

        def call5(drehgeberPin2):
            GPIO.remove_event_detect(drehgeberPin1)
            GPIO.remove_event_detect(drehgeberPin2)
            state = R_START
            x= True
            while(x):
                pinstate = ((GPIO.input(drehgeberPin2) << 1)| GPIO.input(drehgeberPin1))
                state = ttable[state & 0xf][pinstate]
                if state ==  DIR_CW:
                    print ("Rechts")
                    x = False
                elif state == DIR_CCW:
                    print ("Links")
                    x = False
            GPIO.add_event_detect(drehgeberPin1, GPIO.BOTH, callback = call4)
            GPIO.add_event_detect(drehgeberPin2, GPIO.BOTH, callback = call5)

        GPIO.add_event_detect(tasterPin1, GPIO.FALLING, callback = call1, bouncetime = 200)
        GPIO.add_event_detect(tasterPin2, GPIO.FALLING, callback = call2, bouncetime = 200)
        GPIO.add_event_detect(tasterPin3, GPIO.FALLING, callback = call3, bouncetime = 200)
        GPIO.add_event_detect(drehgeberPin1, GPIO.BOTH, callback = call4)
        GPIO.add_event_detect(drehgeberPin2, GPIO.BOTH, callback = call5)

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
                time.sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()
            print ("Programm Beendet")
 
thread2 = BThread()
thread2.start()
app = QApplication(sys.argv)

view = Infoscreen()
view.showMaximized()
view.forward()
##thread1 = AThread()

##thread1.finished.connect(app.exit)
##thread2.finished.connect(app.exit)
## Start them
##thread1.start()


app.exec_()
##sys.exit(app.exec_())
