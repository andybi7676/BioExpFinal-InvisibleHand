import sys
import os
import random

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtBluetooth

class SignalReaderBthConn(QWidget):

    def __init__(self, addr, decisionMaker=None):
        self.addr = addr
        super().__init__()
        self.connectToRobot()
        self.win = QWidget()
        self.win.show()
        self.dataBuffer = []
        self.decisionMaker = decisionMaker

    def connectToRobot(self):
        self.sock = QtBluetooth.QBluetoothSocket(QtBluetooth.QBluetoothServiceInfo.RfcommProtocol)
        self.sock.connected.connect(self.connectedToBluetooth)
        self.sock.readyRead.connect(self.receivedBluetoothMessage)
        self.sock.disconnected.connect(self.disconnectedFromBluetooth)
        self.sock.error.connect(self.socketError)
        port = 1
        self.sock.connectToService(QtBluetooth.QBluetoothAddress(self.addr),port)

    
    def log(self, content):
        print(f"[ SIGNAL_RECEIVER ] - {content}")

    def socketError(self,error):
        self.log(self.sock.errorString())

    def connectedToBluetooth(self):
        self.log("connected")
        self.sock.write('connnection from pc'.encode())

    def disconnectedFromBluetooth(self):
        self.log('Disconnected from bluetooth')

    def receivedBluetoothMessage(self):
        while self.sock.canReadLine():
            signal = str(self.sock.readLine(), "utf-8").strip()
            if not self.decisionMaker.makingDecision:
                self.log(f'received signal: {signal}, sent to decisionMaker')
                self.decisionMaker.makeDecision(signal)
            else:
                self.log(f"received signal: {signal}, but cannot send to decisionMaker")

class DecisionSenderBthConn(QWidget):

    def __init__(self, addr):
        super().__init__()
        self.addr = addr
        self.connectToRobot()
        self.win = QWidget()
        self.win.show()
    
    def log(self, content):
        print(f"[ DICISION_SENDER ] - {content}")
    
    def sendDecision(self, decision: str):
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
        self.log("connected")
        self.sock.write('connnection from pc'.encode())

    def disconnectedFromBluetooth(self):
        self.log('Disconnected from bluetooth')

    def receivedBluetoothMessage(self):
        while self.sock.canReadLine():
            line = str(self.sock.readLine(), "utf-8").strip()
            self.log(line)

class DecisionMaker():

    def __init__(self, decisionSender=None) -> None:
        super().__init__()
        self.decisionSender = decisionSender
        self.makingDecision = False
        self.decisions = ['F', 'B', 'L', 'R', 'A', 'D', 'S']
        pass
    
    def log(self, content):
        print(f"[ DICISION_MAKER ] - {content}")

    def makeDecision(self, signal):
        self.makingDecision = True
        decision = ''
        if (signal.upper() in self.decisions):
            decision = signal.upper()
        else:
            decision = random.choice(self.decisions)
        self.log(f'made decision: \'{decision}\'')
        self.decisionSender.sendDecision(decision)
        self.makingDecision = False



def main():
    # deal with a bluetooth bug on mac
    if sys.platform == 'darwin':
        os.environ['QT_EVENT_DISPATCHER_CORE_FOUNDATION'] = '1'

    app = QApplication(sys.argv)
    decisionSender = DecisionSenderBthConn("00:13:EF:00:27:9D") # BioExpG5-2
    decisionMaker = DecisionMaker(decisionSender=decisionSender)
    signalReceiver = SignalReaderBthConn("98:D3:81:FD:46:F2", decisionMaker=decisionMaker) # BioExpG5-1

    sys.exit(app.exec_())

if __name__ == '__main__':
        main()