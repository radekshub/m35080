import sys
import serial
import serial.tools.list_ports
import array

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QListWidget, QProgressBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QTimer

comlist = serial.tools.list_ports.comports()

ser = serial.Serial()
ser.baudrate = 115200
ser.timeout = 1

DATA = array.array('B', [0]) * 1024


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'M35080 Programmer  |  Copyright (c) 2019 - Radek Sebela'
        self.left = 30
        self.top = 70
        self.width = 800
        self.height = 600
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create a openButton in the window
        self.openButton = QPushButton('Open Port', self)
        self.openButton.move(125, 270)
        self.openButton.resize(95, 40)
        self.openButton.setEnabled(False)
        self.openButton.clicked.connect(self.openButtonOnClick)

        self.portListwidget = QListWidget(self)
        self.portListwidget.move(20, 20)
        self.portListwidget.resize(200, 230)
        self.portListwidget.itemSelectionChanged.connect(self.on_selection_changed)
        index = 0
        for element in comlist:
            self.portListwidget.insertItem(index, str(element.device))
            index += 1
        if index > 0:
            self.portListwidget.setCurrentRow(0)
#270,330,390,450,510
        # Create a reloadButton in the window
        self.reloadButton = QPushButton('Reload Ports', self)
        self.reloadButton.move(20, 270)
        self.reloadButton.resize(95, 40)
        self.reloadButton.clicked.connect(self.reloadButtonOnClick)

        # Create a testButton in the window
        self.testButton = QPushButton('HW Info', self)
        self.testButton.move(20, 330)
        self.testButton.resize(95, 40)
        self.testButton.setEnabled(False)
        self.testButton.clicked.connect(self.testButtonOnClick)

        # Create a readAllButton in the window
        self.readAllButton = QPushButton('Read All', self)
        self.readAllButton.move(125, 330)
        self.readAllButton.resize(95, 40)
        self.readAllButton.setEnabled(False)
        self.readAllButton.clicked.connect(self.readAllButtonOnClick)

        # Create a saveToFileButton in the window
        self.saveToFileButton = QPushButton('Save to File', self)
        self.saveToFileButton.move(20, 390)
        self.saveToFileButton.resize(95, 40)
        self.saveToFileButton.setEnabled(False)
        self.saveToFileButton.clicked.connect(self.saveToFileButtonOnClick)


        # Create a closeButton in the window
        self.closeButton = QPushButton('Close Port', self)
        self.closeButton.move(125, 510)
        self.closeButton.resize(95, 40)
        self.closeButton.setEnabled(False)
        self.closeButton.clicked.connect(self.closeButtonOnClick)

        self.statusLabel = QLabel('Status Info', self)
        self.statusLabel.move(20, 565)
        self.statusLabel.resize(200, 20)

        self.dataListwidget = QListWidget(self)
        self.dataListwidget.move(240, 20)
        self.dataListwidget.resize(540, 530)
        self.dataListwidget.setEnabled(False)
        self.dataListwidget.setFont(QFont("Courier", 10, QFont.Bold))
        #self.dataListwidget.itemSelectionChanged.connect(self.dataListwidget_onSelectionChanged)

        self.progress = QProgressBar(self)
        self.progress.setTextVisible(False)
        self.progress.setGeometry(240, 565, 540, 20)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)

        self.response = bytes('', 'utf-8')
        self.INIT_HW_ID = 0
        self.READING_ID = 1
        self.timerID = self.INIT_HW_ID
        self.totalBytes = 0
        self.address = 0
        self.timerCounter = 0
        self.my_qtimer = QTimer(self)
        self.my_qtimer.timeout.connect(self.onTimer)
        self.show()
    
    @pyqtSlot()
    def on_selection_changed(self):
        if not self.portListwidget.selectedItems():
            self.openButton.setEnabled(False)
        else:
            self.openButton.setEnabled(True)

    def reloadButtonOnClick(self):
        self.portListwidget.clear()
        comlist = serial.tools.list_ports.comports()
        index = 0
        for element in comlist:
            self.portListwidget.insertItem(index, str(element.device))
            index += 1
        if index > 0:
            self.portListwidget.setCurrentRow(0)

    def openButtonOnClick(self):
        self.disableAllUI()
        self.progress.setValue(0)
        self.statusLabel.setText('Hardware initialization in progress.')
        ser.port = self.portListwidget.selectedItems()[0].text()
        ser.open()
        #print(ser)
        self.timerCounter = 0
        self.timerID = self.INIT_HW_ID
        self.my_qtimer.start(100)

    def testButtonOnClick(self):
        testcmd = "CMD:INFO;"
        ser.write(testcmd.encode())
        self.response = ser.read_until('\n')
        #print(self.response)
        QMessageBox.question(self, 'M35080 Programmer', self.response.decode("utf-8"), QMessageBox.Ok, QMessageBox.Ok)

    def readAllButtonOnClick(self):
        self.disableAllUI()
        #QMessageBox.question(self, 'M35080 Programmer', "Be patient!", QMessageBox.Ok, QMessageBox.Ok)
        self.statusLabel.setText('Reading in progress.')
        self.progress.setValue(0)
        self.totalBytes = 0
        self.address = 0
        self.timerCounter = 0
        self.timerID = self.READING_ID
        self.my_qtimer.start(100)

    def saveToFileButtonOnClick(self):
        file = open("M35080.bin", "wb")
        file.write(DATA)
        file.close()

    def closeButtonOnClick(self):
        ser.close()
        self.statusLabel.setText('Hardware disconnected.')
        self.progress.setValue(0)
        self.disableAllUI()
        self.enablePortUI()

    def onTimer(self):
        #print("onTimer\n")
        if self.timerID == self.INIT_HW_ID:
            self.onHardwareInitializationTimer()
        elif self.timerID == self.READING_ID:
            self.onReadingTimer()
        else:
            print("ERROR - onTimer: Bad ID!\n")

    def onHardwareInitializationTimer(self):
        #print("onHardwareInitializationTimer\n")
        self.timerCounter += 1
        self.progress.setValue(self.timerCounter)
        #if self.timerCounter < 25:
            #
        if self.timerCounter == 5 or self.timerCounter == 25 or self.timerCounter == 45 or self.timerCounter == 65 or self.timerCounter == 85:
            self.initializationCmdTest()
        elif self.timerCounter > 5 and self.timerCounter < 100:
            #self.response += ser.read_until('\n', 1)
            if ser.in_waiting > 0:
                self.response += ser.read(ser.in_waiting)
            if len(self.response) >= 7:
                #print(self.response)
                pair = self.response.decode("utf-8").split(";")
                #print(len(pair))
                #print(pair[0])
                if len(pair) > 0 and pair[0] == "M35080":
                    self.my_qtimer.stop()
                    self.statusLabel.setText('Hardware connected.')
                    self.progress.setValue(100)
                    self.enableProcessUI()
                else:
                    self.initializationCmdTest()
        elif self.timerCounter >= 100:
            self.my_qtimer.stop()
            ser.close()
            self.progress.setValue(0)
            self.enablePortUI()
            errorMessage = 'ERROR: Hardware not connected!'
            self.statusLabel.setText(errorMessage)
            QMessageBox.critical(self, 'M35080 Programmer', errorMessage, QMessageBox.Ok)

    def disableAllUI(self):
        self.portListwidget.setEnabled(False)
        self.reloadButton.setEnabled(False)
        self.openButton.setEnabled(False)
        self.testButton.setEnabled(False)
        self.closeButton.setEnabled(False)
        self.dataListwidget.setEnabled(False)
        self.readAllButton.setEnabled(False)

    def enablePortUI(self):
        self.portListwidget.setEnabled(True)
        self.reloadButton.setEnabled(True)
        self.openButton.setEnabled(True)

    def enableProcessUI(self):
        self.testButton.setEnabled(True)
        self.closeButton.setEnabled(True)
        self.dataListwidget.setEnabled(True)
        self.readAllButton.setEnabled(True)

    def initializationCmdTest(self):
        #self.response = ser.read_until('\n', 1000)
        if ser.in_waiting > 0:
            self.response = ser.read(ser.in_waiting)
        #print(self.response)
        self.response = bytes('', 'utf-8')
        readCmd = "CMD:TEST;"
        #print(readCmd)
        ser.write(readCmd.encode())

    def readingCmdRead(self):
        #self.response = ser.read_until('\n', 1000)
        if ser.in_waiting > 0:
            self.response = ser.read(ser.in_waiting)
        self.response = bytes('', 'utf-8')
        readCmd = "CMD:READ," + "0x%04X" % self.address + ",0x%02X" % 32 + ";"
        #print(readCmd)
        ser.write(readCmd.encode())

    def dataToListwidget(self):
        self.dataListwidget.clear()
        for index in range(64):
            line = "0x%04X: " % (index * 16)
            for item in range(16):
                line = line + "%02X " % DATA[index * 16 + item]
            self.dataListwidget.insertItem(self.dataListwidget.count(), line)
        self.saveToFileButton.setEnabled(True)

    def readingNext(self):
        self.timerCounter = 0
        self.address += 32
        if self.address < 1024:
            self.progress.setValue((self.address / 32) * 3)
            self.readingCmdRead()
        else:
            self.my_qtimer.stop()
            self.dataToListwidget()
            self.enableProcessUI()
            if self.totalBytes == 1024:
                self.progress.setValue(100)
                self.statusLabel.setText(str(self.totalBytes) + ' bytes has been read.')
                #QMessageBox.information(self, 'M35080 Programmer - Reading complete.', "OK - Total received bytes from device: " + str(self.totalBytes) + ". Verify data!")
                ##QMessageBox.question(self, 'M35080 - Reading complete.', "OK: Total received bytes from device: " + str(self.totalBytes) + ". Verify data!", QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.progress.setValue(0)
                errorMessage = "ERROR: " + str(self.totalBytes) + " bytes has been read!"
                self.statusLabel.setText(errorMessage)
                QMessageBox.critical(self, 'M35080 Programmer', errorMessage, QMessageBox.Ok)

    def onReadingTimer(self):
        #print("onReadingTimer - self.timerCounter: " + str(self.timerCounter) + "\n")
        if self.timerCounter == 0:
            self.readingCmdRead()
        elif self.timerCounter < 30:
            #self.response += ser.read_until('\n', 100)
            if ser.in_waiting > 0:
                self.response += ser.read(ser.in_waiting)
            if len(self.response) == 395:
                packetBytes = 0
                #print("self.response - len: " + str(len(self.response)))
                #print(self.response)
                separatorSplitted = self.response.decode("utf-8").split(";")
                splittedData = separatorSplitted[0].split(",")
                for xxx in splittedData:
                    dataPair = xxx.split("=")
                    if len(dataPair) == 2:
                        DATA[int(dataPair[0], 0)] = int(dataPair[1], 0)
                        packetBytes += 1
                if packetBytes == 32:
                    self.totalBytes += packetBytes
                    self.readingNext()
        else:
            self.readingNext()
        self.timerCounter += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())