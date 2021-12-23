import numpy as np
import os
from PyQt5 import QtBluetooth

THRESHOLD = 5

class SignalBthConn():

    def __init__(self, addr, dataCollector = None):
        self.addr = addr
        super().__init__()
        self.connectToRobot()
        self.dataBuffer = []
        self.dataCollector = dataCollector

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
        if self.dataCollector:
            self.dataCollector.stopCollecting()

    def receivedBluetoothMessage(self):
        while self.sock.canReadLine():
            signal = str(self.sock.readLine())[2:-3].strip()
            print(signal)
            # if (self.dataCollector and not self.dataCollector.pauseHandling):
            #     self.dataCollector.handleNewSignal(signal)

class DataCollector():

    def __init__(self) -> None:
        super().__init__()
        self.newDataFig = []
        self.threshold = THRESHOLD
        self.recording = False
        self.recordedDataFigs = []
        self.onRecordData = []
        self.pauseHandling = False
    
    @staticmethod
    def parseData(signal) -> np.ndarray:
        gx = int(signal.split(' ')[0])
        gy = int(signal.split(' ')[1])
        gz = int(signal.split(' ')[2])
        return np.array([gx, gy, gz])
    
    def overThreshold(self, frame: np.ndarray) -> bool:
        return np.sqrt(frame.dot(frame)) > self.threshold
    
    def handleNewSignal(self, newSignal):
        frame = DataCollector.parseData(newSignal)
        if self.recording:
            if self.overThreshold(frame):
                self.onRecordData.append(frame) # Keep collecting data
            else:
                self.recording = False
                self.recordedDataFigs.append(np.array(self.onRecordData))
                print(np.array(self.onRecordData))
                self.pauseHandling = True
                print("End recording.")
        else:
            if self.overThreshold(frame):
                self.recording = True # Start recording
                print("Start recording...")
                self.onRecordData = []
                self.onRecordData.append(frame)
            else:
                self.recording = False # Unnecessary
                pass

    def stopCollecting(self):
        pass
        # self.dumpCollectedData()
    
    # def dumpCoollectedData()

if __name__ == "__main__":
    #  "98:D3:81:FD:46:F2" BioExpG5-1
    #  "00:13:EF:00:27:9D" BioExpG5-2
    dataCollector = DataCollector()
    sigBth = SignalBthConn("98:D3:81:FD:46:F2", dataCollector=dataCollector)