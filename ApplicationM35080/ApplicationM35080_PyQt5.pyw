import sys
import serial
import serial.tools.list_ports
import array
import time

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

comlist = serial.tools.list_ports.comports()

ser = serial.Serial()
ser.baudrate = 9600
ser.timeout = 1

DATA = array.array('B', [0]) * 1024

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'M35080'
        self.left = 30
        self.top = 70
        self.width = 800
        self.height = 600
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        ## Create textbox
        #self.textbox = QLineEdit(self)
        ##self.textbox.setText("")
        #self.textbox.move(20, 300)
        #self.textbox.resize(280, 40)

        ## Create textbox2
        #self.textbox2 = QLineEdit(self)
        #self.textbox2.move(20, 400)
        #self.textbox2.resize(280, 40)

        self.portListwidget = QListWidget(self)
        self.portListwidget.move(20, 20)
        self.portListwidget.resize(200, 230)
        self.portListwidget.itemSelectionChanged.connect(self.on_selection_changed)
        index = 0
        for element in comlist:
            self.portListwidget.insertItem(index, str(element.device))
            index += 1
#270,330,390,450,510
        # Create a reloadButton in the window
        self.reloadButton = QPushButton('Reload Ports', self)
        self.reloadButton.move(20, 270)
        self.reloadButton.resize(95, 40)
        self.reloadButton.clicked.connect(self.reloadButtonOnClick)

        # Create a openButton in the window
        self.openButton = QPushButton('Open Port', self)
        self.openButton.move(125, 270)
        self.openButton.resize(95, 40)
        self.openButton.setEnabled(False)
        self.openButton.clicked.connect(self.openButtonOnClick)

        # Create a testButton in the window
        self.testButton = QPushButton('Read Info', self)
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
        #self.saveToFileButton.setEnabled(False)
        self.saveToFileButton.clicked.connect(self.saveToFileButtonOnClick)


        # Create a closeButton in the window
        self.closeButton = QPushButton('Close', self)
        self.closeButton.move(20, 510)
        self.closeButton.resize(200, 40)
        self.closeButton.setEnabled(False)
        self.closeButton.clicked.connect(self.closeButtonOnClick)

        self.dataListwidget = QListWidget(self)
        self.dataListwidget.move(240, 20)
        self.dataListwidget.resize(540, 530)
        self.dataListwidget.setEnabled(False)
        #self.dataListwidget.itemSelectionChanged.connect(self.dataListwidget_onSelectionChanged)

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

    def openButtonOnClick(self):
        ser.port = self.portListwidget.selectedItems()[0].text()
        ser.open()
        print(ser)
        hello = ser.read_until('\n')
        print(hello)
        self.portListwidget.setEnabled(False)
        self.reloadButton.setEnabled(False)        
        self.openButton.setEnabled(False)
        self.testButton.setEnabled(True)
        self.closeButton.setEnabled(True)
        self.dataListwidget.setEnabled(True)
        self.readAllButton.setEnabled(True)

    def testButtonOnClick(self):
        testcmd = "CMD:INFO;"
        ser.write(testcmd.encode())
        response = ser.read_until('\n')
        print(response)
        QMessageBox.question(self, 'M35080 - Communication Test', response.decode("utf-8"), QMessageBox.Ok, QMessageBox.Ok)

    def readAllButtonOnClick(self):
        QMessageBox.question(self, 'M35080', "Be patient!", QMessageBox.Ok, QMessageBox.Ok)
        time.sleep(3)
        totalBytes = 0
        for addressIndex in range(32):
            address = addressIndex * 32
            readCmd = "CMD:READ," + "0x%04X" % address + ",0x%02X" % 32 + ";"
            print(readCmd)
            ser.write(readCmd.encode())
            response = ser.read_until('\n')
            print(response)
            separatorSplitted = str(response).split(";")
            splittedData = separatorSplitted[0].split(",")
            for xxx in splittedData:
                dataPair = xxx.split("=")
                if len(dataPair) == 2:
                    DATA[int(dataPair[0], 0)] = int(dataPair[1], 0)
                    totalBytes = totalBytes + 1
        self.dataListwidget.clear()
        for index in range(32):
            line = "0x%04X: " % (index * 32)
            for item in range(32):
                line = line + "%02X," % DATA[index * 32 + item]
            self.dataListwidget.insertItem(self.dataListwidget.count(), line)
        if totalBytes == 1024:
            QMessageBox.question(self, 'M35080 - Reading complete.', "OK: Total received bytes from device: " + str(totalBytes) + ". Verify data!", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'M35080 - Reading ERROR!', "ERROR: Total received bytes from device: " + str(totalBytes) + "!", QMessageBox.Ok)

    def saveToFileButtonOnClick(self):
        file = open("M35080.bin", "wb")
        file.write(DATA)
        file.close()

    def closeButtonOnClick(self):
        ser.close()
        self.portListwidget.setEnabled(True)
        self.reloadButton.setEnabled(True)        
        self.openButton.setEnabled(True)
        self.testButton.setEnabled(False)
        self.closeButton.setEnabled(False)
        self.dataListwidget.setEnabled(False)
        self.readAllButton.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())