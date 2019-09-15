import sys
import serial
import serial.tools.list_ports
import io

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

comlist = serial.tools.list_ports.comports()

ser = serial.Serial()
ser.baudrate = 9600
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

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

        self.listwidget = QListWidget(self)
        self.listwidget.move(20, 20)
        self.listwidget.resize(200, 150)
        self.listwidget.itemSelectionChanged.connect(self.on_selection_changed)
        index = 0
        for element in comlist:
            self.listwidget.insertItem(index, str(element.device))
            index += 1

        # Create a reloadButton in the window
        self.reloadButton = QPushButton('Reload List', self)
        self.reloadButton.move(20, 190)
        self.reloadButton.resize(200, 40)
        self.reloadButton.clicked.connect(self.reloadButtonOnClick)

        # Create a openButton in the window
        self.openButton = QPushButton('Open', self)
        self.openButton.move(20, 250)
        self.openButton.resize(200, 40)
        self.openButton.setEnabled(False)
        self.openButton.clicked.connect(self.openButtonOnClick)

        # Create a closeButton in the window
        self.closeButton = QPushButton('Close', self)
        self.closeButton.move(20, 310)
        self.closeButton.resize(200, 40)
        self.closeButton.setEnabled(False)
        self.closeButton.clicked.connect(self.closeButtonOnClick)

        self.show()
    
    @pyqtSlot()
    def on_selection_changed(self):
        if not self.listwidget.selectedItems():
            self.openButton.setEnabled(False)
        else:
            self.openButton.setEnabled(True)

    def reloadButtonOnClick(self):
        self.listwidget.clear()
        comlist = serial.tools.list_ports.comports()
        index = 0
        for element in comlist:
            self.listwidget.insertItem(index, str(element.device))
            index += 1
#        QMessageBox.question(self, 'Message - pythonspot.com', "ser.is_open: " + ser.is_open, QMessageBox.Ok, QMessageBox.Ok)

    def openButtonOnClick(self):
        ser.port = self.listwidget.selectedItems()[0].text()
        ser.open()
        sio.write("\n")
        sio.flush()
        hello = sio.readline()
        print(hello == "hello\n")
        self.listwidget.setEnabled(False)
        self.reloadButton.setEnabled(False)        
        self.openButton.setEnabled(False)
        self.closeButton.setEnabled(True)

    def closeButtonOnClick(self):
        ser.close()
        self.listwidget.setEnabled(True)
        self.reloadButton.setEnabled(True)        
        self.openButton.setEnabled(True)
        self.closeButton.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())