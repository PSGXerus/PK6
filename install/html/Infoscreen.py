#!/usr/bin/env python3
import PyQt5
import sys
import os.path
import os
import inspect
import RPi.GPIO as GPIO
import threading
import time
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtNetwork import *

## Get the current working directory
def setDir():
    if len(sys.argv) is 1:
    	print("Please specify HTML directory as first argument")
    	sys.exit()
    directory = os.path.join(os.path.abspath(sys.argv[1]), '')
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
    return fileList

## Global variables ##
fileCounter = 0 # Counter to save the last shown file index #
fileList = list() # List for the html files

###########
### GUI ###
###########

## The GUI class
class Infoscreen(QWebView):

    def __init__(self):
        super(Infoscreen, self).__init__()
        self.setWindowTitle('Infoscreen')
        self.titleChanged.connect(self.adjustTitle)

    def adjustTitle(self):
        self.setWindowTitle(self.title())

    def disableJS(self):
        settings = QWebSettings.globalSettings()
        settings.setAttribute(QWebSettings.JavascriptEnabled, False)

    ## Close app when the specified key was pressed
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def switchPage(self, fileIndex):
        fileList = initFileList()
        try:
            file = fileList[fileIndex]
            html = openFile(file)
            self.setHtml(html,QUrl.fromLocalFile(setDir()))
        except IndexError as e:
            print(e)

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

    def connect_input(self, inputthread):
        inputthread.update_signal.connect(self.update)



############
### GPIO ###
############

## Thread for the GPIO class
class GPIO_Thread(QThread):

    update_signal = pyqtSignal(str,name='update')

    def __init__(self):
        super(GPIO_Thread, self).__init__()
        #threading.Thread.__init__(self)
        self.state = 0


    def run(self):
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
        self.state = R_START

        def call1(channel):
            self.update_signal.emit("fwd")

        def call2(channel):
            self.update_signal.emit("bwd")

        def call3(channel):
            self.update_signal.emit("home")


        def call4(channel):
            pinstate = ((GPIO.input(drehgeberPin2) << 1)| GPIO.input(drehgeberPin1))
            self.state = ttable[self.state & 0xf][pinstate]
            if self.state ==  DIR_CW:
                self.update_signal.emit("down")
            elif self.state == DIR_CCW:
                self.update_signal.emit("up")

        GPIO.add_event_detect(tasterPin1, GPIO.FALLING, callback = call1, bouncetime = 200)
        GPIO.add_event_detect(tasterPin2, GPIO.FALLING, callback = call2, bouncetime = 200)
        GPIO.add_event_detect(tasterPin3, GPIO.FALLING, callback = call3, bouncetime = 200)

        GPIO.add_event_detect(drehgeberPin1, GPIO.BOTH, callback = call4)
        GPIO.add_event_detect(drehgeberPin2, GPIO.BOTH, callback = call4)

        while True:
            time.sleep(1)

    def __del__(self):
        GPIO.cleanup()

############
### MAIN ###
############

def main():

    app = QApplication(sys.argv)

    ## Create the thread
    screen = Infoscreen()
    screen.switchPage(0)
    screen.showFullScreen()

    inputthread = GPIO_Thread()
    inputthread.start()
    screen.connect_input(inputthread)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
