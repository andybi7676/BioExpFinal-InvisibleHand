from PyQt5 import QtBluetooth

class LeftSignalBthConn():

    def __init__(self, addr, handler = None):
        self.addr = addr
        super().__init__()
        self.connectToLeftHand()
        self.dataBuffer = []
        self.handler = handler

    def connectToLeftHand(self):
        self.sock = QtBluetooth.QBluetoothSocket(QtBluetooth.QBluetoothServiceInfo.RfcommProtocol)
        self.sock.connected.connect(self.connectedToBluetooth)
        self.sock.readyRead.connect(self.receivedBluetoothMessage)
        self.sock.disconnected.connect(self.disconnectedFromBluetooth)
        self.sock.error.connect(self.socketError)
        port = 1
        self.sock.connectToService(QtBluetooth.QBluetoothAddress(self.addr),port)

    def log(self, content):
        print(f"[ LEFTHAND ] - {content}")

    def socketError(self,error):
        self.log(self.sock.errorString())

    def connectedToBluetooth(self):
        self.log("Connected")

    def disconnectedFromBluetooth(self):
        self.log('Disconnected from bluetooth')

    def receivedBluetoothMessage(self):
        while self.sock.canReadLine():
            signal = str(self.sock.readLine())[2:-3].strip()
            # self.log(signal)
            if self.handler:
                self.handler.handleLeftSignal(signal)

class RightSignalBthConn():

    def __init__(self, addr, handler = None):
        self.addr = addr
        super().__init__()
        self.connectToRight()
        self.handler = handler

    def connectToRight(self):
        self.sock = QtBluetooth.QBluetoothSocket(QtBluetooth.QBluetoothServiceInfo.RfcommProtocol)
        self.sock.connected.connect(self.connectedToBluetooth)
        self.sock.readyRead.connect(self.receivedBluetoothMessage)
        self.sock.disconnected.connect(self.disconnectedFromBluetooth)
        self.sock.error.connect(self.socketError)
        port = 1
        self.sock.connectToService(QtBluetooth.QBluetoothAddress(self.addr),port)

    def log(self, content):
        print(f"[ RIGHTHAND ] - {content}")

    def socketError(self,error):
        self.log(self.sock.errorString())

    def connectedToBluetooth(self):
        self.log("Connected")

    def disconnectedFromBluetooth(self):
        self.log('Disconnected from bluetooth')

    def receivedBluetoothMessage(self):
        while self.sock.canReadLine():
            signal = str(self.sock.readLine())[2:-3].strip()
            # self.log(signal)
            if self.handler:
                self.handler.handleRightSignal(signal)