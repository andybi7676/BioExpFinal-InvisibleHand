import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtBluetooth

class bluetoothConnection(QWidget):

    def __init__(self, addr):
        self.addr = addr
        super().__init__()
        self.connectToRobot()
        self.win = QWidget()
        self.win.show()

    def connectToRobot(self):
        self.sock = QtBluetooth.QBluetoothSocket(QtBluetooth.QBluetoothServiceInfo.RfcommProtocol)

        self.sock.connected.connect(self.connectedToBluetooth)
        self.sock.readyRead.connect(self.receivedBluetoothMessage)
        self.sock.disconnected.connect(self.disconnectedFromBluetooth)
        self.sock.error.connect(self.socketError)
        port = 1
        self.sock.connectToService(QtBluetooth.QBluetoothAddress(self.addr),port)

    def socketError(self,error):
        print(self.sock.errorString())

    def connectedToBluetooth(self):
        print("connected")
        self.sock.write('connnection from pc'.encode())

    def disconnectedFromBluetooth(self):
        print('Disconnected from bluetooth')

    def receivedBluetoothMessage(self):
        while self.sock.canReadLine():
            line = str(self.sock.readLine(), "utf-8").strip()
            print(line)



def main():
    # deal with a bluetooth bug on mac
    if sys.platform == 'darwin':
        os.environ['QT_EVENT_DISPATCHER_CORE_FOUNDATION'] = '1'

    app = QApplication(sys.argv)
    btc = bluetoothConnection("00:13:EF:00:27:9D")
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()