import numpy as np
import os
import sys
import random
import glob

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtBluetooth
from dataCollectionUI import Ui_MainWindow


FRAME_LENGTH_THRESHOLD = 20
ACC_PRECISION_FACTOR = 1000
THRESHOLD_INIT = 0.08
STATIC_LIMIT = 5
ACC_AVG_INIT = 0.98 
VALID_CLASSNAMES = ['backward', 'others', 'forward']
root_dir = './raw_data'

class CollectDataWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.label_to_class = {'forward': '1', 'stop': '0', 'backward': '-1'}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.threshold = THRESHOLD_INIT
        self.acc_avg = ACC_AVG_INIT
        self.duplicateStatic = 0
        self.frame = np.array([0.0 for _ in range(6)])
        self.curAction = []
        self.isRecording = False
        self.className = 'null'
        self.actionsDict = {}
        for className in VALID_CLASSNAMES: self.actionsDict[className] = []
        self.setup_control()

    def setup_control(self):
        self.ui.thresholdLabel.setText(f"Threshold: {THRESHOLD_INIT}")
        self.ui.thresholdLineEdit.setText(str(THRESHOLD_INIT))
        self.ui.thresholdPushButton.clicked.connect(self.setThreshold)
        self.ui.classNameLabel.setText(f"Class Name: {self.className}")
        self.ui.classNameLineEdit.setText(f"{self.className}")
        self.ui.classNamePushButton.clicked.connect(self.setClassName)
        self.ui.isRecordingPushButton.clicked.connect(self.setIsRecording)
        self.ui.dumpDataPushButton.clicked.connect(self.dumpData)
        pass

    def isMoving(self) -> bool:
        return self.duplicateStatic < STATIC_LIMIT

    def setThreshold(self):
        self.threshold = float(self.ui.thresholdLineEdit.text())
        self.ui.thresholdLabel.setText(f"Threshold: {self.threshold}")
    
    def setClassName(self):
        newClassName = self.ui.classNameLineEdit.text()
        if not newClassName in VALID_CLASSNAMES:
            print("[ ERROR ] - Invalid class name!!")
        else:
            self.ui.classNameLabel.setText(f"Class Name: {newClassName}")
            self.className = newClassName
    
    def setIsRecording(self):
        self.isRecording = self.ui.isRecordingPushButton.isChecked()
        if self.isRecording:
            print(f"[ LOG ] - Start recording, class name={self.className}!")
    
    def checkMoving(self, mag):
        if abs(mag - self.acc_avg) > self.threshold:
            self.duplicateStatic = 0 # Is moving
        else:
            self.duplicateStatic = min(STATIC_LIMIT, self.duplicateStatic+1)
        self.ui.movingCheckBox.setChecked(self.isMoving())
        if self.isMoving():
            self.curAction.append(self.frame)
        if not self.isMoving():
            self.acc_avg = max(min(self.acc_avg*0.95 + mag*0.05, 1.0), 0.96)
            if len(self.curAction) > 0:
                print(f"[ Action ] - An action data formed!, frame-length={len(self.curAction)}, className={self.className}")
                # print(np.array(self.curAction))
                if len(self.curAction) > FRAME_LENGTH_THRESHOLD and self.isRecording: # Todo: open another thread for dump file.
                    self.storeAction()
                # Todo: dump action data
                self.curAction.clear()
    
    def storeAction(self):
        if not self.className in VALID_CLASSNAMES:
            print("[ ERROR ] - Invalid class name!!")
            return
        self.actionsDict[self.className].append(np.array(self.curAction))
        print(f"[ STORE ] - An action has been stored, action frame-length: {len(self.curAction)}")
    
    def dumpData(self):
        for className in VALID_CLASSNAMES:
            cur_dir = os.path.join(root_dir, className)
            if not os.path.exists(cur_dir): os.makedirs(cur_dir)
            actions = glob.glob(f'{cur_dir}/{className}-*.npy')
            actions = sorted(actions, key=lambda f_pth: int(f_pth.split('-')[-1].split('.')[0]))
            start_id = 0
            if len(actions) != 0:
                start_id = int(actions[-1].split('-')[-1].split('.')[0]) + 1
            end_id = start_id
            for action in self.actionsDict[className]:
                np.save(os.path.join(cur_dir, f"{className}-{end_id}.npy"), action)
                end_id += 1
            print(f"[ DUMP ] - Totally {end_id - start_id} files dump to class \'{className}\'!!")
            

    def bthConnected(self):
        self.ui.sigRcvConnCheckBox.setChecked(True)
    
    def bthDisconnected(self):
        self.ui.sigRcvConnCheckBox.setChecked(False)
    
    def handleSignal(self, signal: str):
        if len(signal.split(' ')) > 5:
            # Read parse valid signal string to the corresponding values. (accX, accY, accZ => accelerations; angX, angY, angZ => angle of three dimensions).
            accX = int(signal.split(' ')[0]) / ACC_PRECISION_FACTOR
            accY = int(signal.split(' ')[1]) / ACC_PRECISION_FACTOR
            accZ = int(signal.split(' ')[2]) / ACC_PRECISION_FACTOR
            angX = int(signal.split(' ')[3])
            angY = int(signal.split(' ')[4])
            angZ = int(signal.split(' ')[5])
            mag = (accX**2 + accY**2 + accZ**2)**0.5
            # Show values in UI.
            self.ui.accXLineEdit.setText(str(accX))
            self.ui.accYLineEdit.setText(str(accY))
            self.ui.accZLineEdit.setText(str(accZ))
            self.ui.angXLineEdit.setText(str(angX))
            self.ui.angYLineEdit.setText(str(angY))
            self.ui.angZLineEdit.setText(str(angZ))
            self.ui.magLineEdit.setText( str(round(mag, 2)))
            self.frame = np.array([accX, accY, accZ, angX, angY, angZ])
            self.checkMoving(mag)
        else:
            print(f"[ SIGNAL ] - cannot handle signal \'{signal}\'")


class SignalBthConn():

    def __init__(self, addr, dataCollectionWindow: CollectDataWindow = None):
        self.addr = addr
        super().__init__()
        self.connectToRobot()
        self.dataBuffer = []
        self.dataCollectionWindow = dataCollectionWindow

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
        if self.dataCollectionWindow:
            self.dataCollectionWindow.bthConnected()
        self.sock.write('connnection from pc'.encode())

    def disconnectedFromBluetooth(self):
        self.log('Disconnected from bluetooth')
        # if self.dataCollectionWindow:
        #     self.dataCollectionWindow.bthDisconnected()

    def receivedBluetoothMessage(self):
        while self.sock.canReadLine():
            signal = str(self.sock.readLine())[2:-3].strip()
            # self.log(signal)
            if self.dataCollectionWindow:
                self.dataCollectionWindow.handleSignal(signal)
            # print(signal)
            # if (self.dataCollector and not self.dataCollector.pauseHandling):
            #     self.dataCollector.handleNewSignal(signal)

def main():
    app = QtWidgets.QApplication(sys.argv)
    dataCollectionWindow = CollectDataWindow()
    dataCollectionWindow.show()
    sigBth = SignalBthConn("98:D3:81:FD:46:F2", dataCollectionWindow=dataCollectionWindow)

    sys.exit(app.exec_())

if __name__ == "__main__":
    #  "98:D3:81:FD:46:F2" BioExpG5-1
    #  "00:13:EF:00:27:9D" BioExpG5-2
    #  "00:19:06:34:F0:FD" BioExpG5-3
    # dataCollector = DataCollector()
    main()