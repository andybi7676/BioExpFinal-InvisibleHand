from const import *
import numpy as np
import os
import sys
import random
import glob

from PyQt5 import QtCore, QtWidgets
from panel.mainUI import Ui_MainWindow
from bth_rcv import LeftSignalBthConn, RightSignalBthConn
# bth rcv

class MainControlPanel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.left = LeftController()
        self.right = RightController()
        self.prevState = State() # Direction, Acceleration, Activate, Left, Right
        self.curState  = State()
        self.left.ui = self.ui
        self.right.ui = self.ui
        self.left.curState = self.curState
        self.right.curState = self.curState
        self.decisionSender = None
        self.setupControl()
    
    def setupControl(self):
        self.ui.initializePushButton.clicked.connect(self.setInitialize)
        pass
        
    def setInitialize(self):
        self.left.initializationProgress = 0
        self.left.handleState  = 0
        self.right.handleState = 0

    def handleLeftSignal(self, signal: str) -> None:
        if len(signal.split(' ')) != 3:
            print(f"[ CONTROLLER ] - Can not handle left signal: \'{signal}\'.")
            return
        angX = int(signal.split(' ')[0])
        angY = int(signal.split(' ')[1])
        angZ = int(signal.split(' ')[2])
        signal = [angX, angY, angZ]
        if self.left.handleState == -1: return
        if self.left.handleState == 0:
            self.left.initializing(signal)
        elif self.left.handleState == 1:
            self.left.driving(signal)
        self.updateStateAndSend()
        pass

    def handleRightSignal(self, signal: str) -> None:
        if len(signal.split(' ')) != 6:
            print(f"[ CONTROLLER ] - Can not handle right signal: \'{signal}\'.")
            return
        accX = int(signal.split(' ')[0]) / ACC_PRECISION_FACTOR
        accY = int(signal.split(' ')[1]) / ACC_PRECISION_FACTOR
        accZ = int(signal.split(' ')[2]) / ACC_PRECISION_FACTOR
        angX = int(signal.split(' ')[3])
        angY = int(signal.split(' ')[4])
        angZ = int(signal.split(' ')[5])
        signal = [accX, accY, accZ, angX, angY, angZ]
        if self.right.handleState == -1: return
        if self.right.handleState == 0:
            self.right.initializing(signal)
        elif self.right.handleState == 1:
            self.right.driving(signal)
        self.updateStateAndSend()
        pass

    def updateStateAndSend(self):
        if str(self.curState) != str(self.prevState):
            self.prevState.acceleration = self.curState.acceleration
            self.prevState.direction    = self.curState.direction
            self.prevState.activate     = self.curState.activate
            self.prevState.left         = self.curState.left
            self.prevState.right        = self.curState.right
            if (self.decisionSender):
                self.decisionSender.sendDicision(str(self.curState))
            self.updateUI()
    
    def updateUI(self):
        self.ui.accelerationValue.setText(str(self.curState.acceleration))
        self.ui.directionValue.setText(str(self.curState.direction))
        self.ui.gearSlider.setValue(self.curState.activate)
        self.ui.leftPushButton.setChecked(self.curState.left)
        self.ui.rightPushButton.setChecked(self.curState.right)

class State():
    def __init__(self) -> None:
        self.acceleration: int = -5
        self.direction   : int = 0
        self.activate    : int = 0
        self.left        :bool = False
        self.right       :bool = False
    
    def __repr__(self) -> str:
        return f"{self.direction} {self.acceleration} {self.activate} {str(self.left)[0]} {str(self.right)[0]}\n"
    
    def __str__(self) -> str:
        return f"{self.direction} {self.acceleration} {self.activate} {str(self.left)[0]} {str(self.right)[0]}\n"


class LeftController():
    def __init__(self) -> None:
        self.handleState = -1 # wait for initialization
        self.initializationProgress = 0
        self.angleOrigs = [0, 0, 0]
        self.dirAngleSeg = 10
        self.accelAngleSeg = 12
        self.ui: Ui_MainWindow = None
        self.curState: State = None

    def initializing(self, signal: list):
        # self.angleOrigs = [0, 0, 0]
        for i in range(len(signal)):
            self.angleOrigs[i] += signal[i] / INITIALIZE_LENGTH
        self.initializationProgress += 1 / INITIALIZE_LENGTH * 100
        self.ui.initializeProgressBar.setValue(round(self.initializationProgress))
        if round(self.initializationProgress) == 100:
            print(self.angleOrigs)
            self.handleState  = 1
    
    def driving(self, signal: list):
        self.curState.direction =     -( (signal[2] + self.dirAngleSeg/2   - self.angleOrigs[2]) // self.dirAngleSeg   )
        self.curState.acceleration =  -( (signal[1] + self.accelAngleSeg/2 - self.angleOrigs[1]) // self.accelAngleSeg )
        pass

class RightController():
    def __init__(self) -> None:
        self.handleState = -1
        self.angleOrigs = [0, 0, 0]
        self.curAction = []
        self.threshold = THRESHOLD_INIT
        self.acc_avg = ACC_AVG_INIT
        self.duplicateStatic = STATIC_LIMIT
        self.ui: Ui_MainWindow = None
        self.curState: State = None
    
    def isMoving(self) -> bool:
        return self.duplicateStatic < STATIC_LIMIT

    def initializing(self, signal: list):
        pass
    
    def driving(self, signal: list):
        mag = sum([acc**2 for acc in signal[:3]])**0.5
        if signal[-2] > 50:
            self.curState.activate = 0
            self.curState.left     = False
            self.curState.right    = False
            return
        if abs(mag - self.acc_avg) > self.threshold:
            self.duplicateStatic = 0 # Is moving
        else:
            self.duplicateStatic = min(STATIC_LIMIT, self.duplicateStatic+1)
        # self.ui.movingCheckBox.setChecked(self.isMoving())
        if self.isMoving():
            self.curAction.append(self.frame)
        if not self.isMoving():
            self.acc_avg = max(min(self.acc_avg*0.95 + mag*0.05, 1.0), 0.96)
            if len(self.curAction) > 0:
                print(f"[ Action ] - An action data formed!, frame-length={len(self.curAction)}, className={self.className}")
                # print(np.array(self.curAction))
                if len(self.curAction) > FRAME_LENGTH_THRESHOLD and self.isRecording: # Todo: open another thread for dump file.
                    self.verrifyAction() # TODOs
                self.curAction.clear()

    def verrifyAction():
        pass
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainControlPanel = MainControlPanel()
    left_bth = LeftSignalBthConn(BioExpG5_3, mainControlPanel)
    right_bth = RightSignalBthConn(BioExpG5_1, mainControlPanel)
    mainControlPanel.left_bth = left_bth
    mainControlPanel.right_bth = right_bth
    mainControlPanel.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    main()