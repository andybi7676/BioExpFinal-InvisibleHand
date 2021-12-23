import sys
import os
import random

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtBluetooth

from controlPanelUI import Ui_MainWindow


class ControlPanel(QtWidgets.QMainWindow):
    def __init__(self, decisionSender=None):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        self.decisionSender = decisionSender

    def setup_control(self):
        self.speed = self.ui.speedSlider.value()
        self.direction = self.ui.directionSlider.value()
        self.mode = self.ui.modeSlider.value()
        self.leftLight = bool(self.ui.leftPushButton.isChecked())
        self.rightLight = bool(self.ui.rightPushButton.isChecked())
        self.ui.speedSlider.valueChanged.connect(self.changeSpeed)
        self.ui.directionSlider.valueChanged.connect(self.changeDirection)
        self.ui.modeSlider.valueChanged.connect(self.changeMode)
        self.ui.leftPushButton.clicked.connect(self.handleLeftButton)
        self.ui.rightPushButton.clicked.connect(self.handleRightButton)

    def changeSpeed(self):
        self.speed = self.ui.speedSlider.value()
        self.ui.speedLabel.setText(f"{self.speed}")
        self.sendState()
    
    def changeDirection(self):
        self.direction = self.ui.directionSlider.value()
        self.ui.directionLabel.setText(f"{self.direction}")
        self.sendState()
    
    def changeMode(self):
        self.mode = self.ui.modeSlider.value()
        self.ui.modeLabel.setText(f"Mode: {self.mode}")
        self.sendState()

    def handleLeftButton(self):
        self.leftLight = bool(self.ui.leftPushButton.isChecked())
        self.sendState()

    def handleRightButton(self):
        self.rightLight = bool(self.ui.rightPushButton.isChecked())
        self.sendState()    

    def sendState(self):
        if not self.decisionSender:
            print("No decision sender!!")
            return
        if (self.decisionSender.canSend):
            print(f"sendState: ({self.speed}, {self.direction}, {self.mode}, {self.leftLight.__repr__()[0]}, {self.rightLight.__repr__()[0]})")
            self.decisionSender.sendDecision(f"{self.speed} {self.direction} {self.mode} {self.leftLight.__repr__()[0]} {self.rightLight.__repr__()[0]}\n")
        else:
            print(f"Can not send state: ({self.speed}, {self.direction}, {self.mode}, {self.leftLight.__repr__()[0]}, {self.rightLight.__repr__()[0]})")

class DecisionSenderBthConn():

    def __init__(self, addr):
        super().__init__()
        self.addr = addr
        self.connectToRobot()
        self.connected = False
        self.canSend = False
    
    def log(self, content):
        print(f"[ DICISION_SENDER ] - {content}")
    
    def sendDecision(self, decision: str):
        if (self.connected):
            self.sock.write(decision.encode())
            self.log(f"sent decision: \'{decision}\'")

    def connectToRobot(self):
        self.sock = QtBluetooth.QBluetoothSocket(QtBluetooth.QBluetoothServiceInfo.RfcommProtocol)
        self.sock.connected.connect(self.connectedToBluetooth)
        self.sock.readyRead.connect(self.receivedBluetoothMessage)
        self.sock.disconnected.connect(self.disconnectedFromBluetooth)
        self.sock.error.connect(self.socketError)
        port = 1
        self.sock.connectToService(QtBluetooth.QBluetoothAddress(self.addr),port)

    def socketError(self,error):
        self.log(self.sock.errorString())

    def connectedToBluetooth(self):
        self.connected = True
        self.canSend = True
        self.log("connected")
        self.sock.write('connnection from pc'.encode())

    def disconnectedFromBluetooth(self):
        self.canSend = False
        self.log('Disconnected from bluetooth')

    def receivedBluetoothMessage(self):
        while self.sock.canReadLine():
            line = str(self.sock.readLine(), encoding='utf-8').strip()
            self.log(line)

def main():
    app = QtWidgets.QApplication(sys.argv)
    bthSender = DecisionSenderBthConn("98:D3:81:FD:46:F2")
    # bthSender = DecisionSenderBthConn("00:13:EF:00:27:9D")
    window = ControlPanel(bthSender)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    #  "98:D3:81:FD:46:F2" BioExpG5-1
    #  "00:13:EF:00:27:9D" BioExpG5-2
    main()