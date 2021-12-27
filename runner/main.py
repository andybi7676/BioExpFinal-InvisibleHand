from const import *
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import sys
import random
import glob

from PyQt5 import QtCore, QtWidgets
from panel.mainUI import Ui_MainWindow
from bth_rcv import LeftSignalBthConn, RightSignalBthConn, DecisionSenderBthConn
from model import ResNetClassifier
# bth rcv

class MainControlPanel(QtWidgets.QMainWindow):
    def __init__(self, decisionSender: DecisionSenderBthConn=None):
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
        self.decisionSender = decisionSender
        self.setupControl()

    def setupControl(self):
        self.ui.initializeLeftPushButton.clicked.connect(self.setInitializeLeft)
        self.ui.initializeRightPushButton.clicked.connect(self.setInitializeRight)
        self.ui.gearSlider.valueChanged.connect(self.changeGearMode)
        self.ui.leftPushButton.clicked.connect(self.setLeftLight)
        self.ui.rightPushButton.clicked.connect(self.setRightLight)
    
    def changeGearMode(self):
        self.curState.activate = self.ui.gearSlider.value()
        self.updateStateAndSend()

    def setInitializeLeft(self):
        self.left.angleOrigs = [0, 0, 0]
        self.left.initializationProgress = 0
        self.left.handleState  = 0
    
    def setInitializeRight(self):
        self.right.inputOrigs = [0, 0, 0, 0, 0, 0]
        self.right.initializationProgress = 0
        self.right.handleState = 0
    
    def setLeftLight(self):
        self.curState.left = self.ui.leftPushButton.isChecked()
        self.updateStateAndSend()
    
    def setRightLight(self):
        self.curState.right = self.ui.rightPushButton.isChecked()
        self.updateStateAndSend()

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
            if (self.decisionSender and self.decisionSender.canSend):
                self.decisionSender.sendDecision(str(self.curState))
            self.updateUI()
    
    def updateUI(self):
        self.ui.accelerationValue.setText(str(self.curState.acceleration))
        self.ui.accelerationSlider.setValue(self.curState.acceleration)
        self.ui.directionValue.setText(str(self.curState.direction))
        self.ui.directionSlider.setValue(self.curState.direction)
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
        return f"{self.acceleration} {self.direction} {self.activate} {str(self.left)[0]} {str(self.right)[0]}\n"
    
    def __str__(self) -> str:
        return f"{self.acceleration} {self.direction} {self.activate} {str(self.left)[0]} {str(self.right)[0]}\n"

class LeftController():
    def __init__(self) -> None:
        self.handleState = -1 # wait for initialization
        self.initializationProgress = 0
        self.angleOrigs = [0, 0, 0]
        self.dirAngleSeg = 10
        self.accelAngleSeg = 10
        self.ui: Ui_MainWindow = None
        self.curState: State = None

    def initializing(self, signal: list):
        # self.angleOrigs = [0, 0, 0]
        for i in range(len(signal)):
            self.angleOrigs[i] += signal[i] / INITIALIZE_LENGTH
        self.initializationProgress += 1
        self.ui.initializeLeftProgressBar.setValue(round(self.initializationProgress / INITIALIZE_LENGTH * 100))
        if self.initializationProgress == INITIALIZE_LENGTH:
            print(f"[ LEFTHAND ] - Initialize value: {self.angleOrigs}")
            self.handleState  = 1
    
    def driving(self, signal: list):
        dirAng = signal[2] - self.angleOrigs[2]
        accelAng = signal[1] - self.angleOrigs[1]
        self.curState.direction = -int(np.sign(dirAng) * min(5, abs(dirAng) // self.dirAngleSeg))
        self.curState.acceleration =  -int(np.sign(accelAng) * min(5, abs(accelAng) // self.accelAngleSeg))
        pass

class RightController():
    def __init__(self) -> None:
        self.handleState = -1
        self.inputOrigs = [0, 0, 0]
        self.initializationProgress = 0
        self.curAction = []
        self.threshold = THRESHOLD_INIT
        self.acc_avg = ACC_AVG_INIT
        self.duplicateStatic = STATIC_LIMIT
        self.ui: Ui_MainWindow = None
        self.curState: State = None
        self.initializeModel()
    
    def initializeModel(self):
        self.device = "cpu"
        print(f"[Info]: Use {self.device} now!")
        self.model = ResNetClassifier(
            label_num=3,
            in_channels=[6, 16, 16],
            out_channels=[16, 16, 8],
            downsample_scales=[1, 1, 1],
            kernel_size=3,
            z_channels=8,
            dilation=True,
            leaky_relu=True,
            dropout=0.0,
            stack_kernel_size=3,
            stack_layers=2,
            nin_layers=0,
            stacks=[3, 3, 3],
        ).to(self.device)
        model_path = os.path.join('../circle_ml/results', 'resnet.ckpt')
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
    
    def isMoving(self) -> bool:
        return self.duplicateStatic < STATIC_LIMIT

    def initializing(self, signal: list):
        for i in range(len(signal)):
            self.inputOrigs[i] += signal[i] / INITIALIZE_LENGTH
        self.initializationProgress += 1
        self.ui.initializeRightProgressBar.setValue(round(self.initializationProgress / INITIALIZE_LENGTH * 100))
        if self.initializationProgress == INITIALIZE_LENGTH:
            print(f"[ RIGHTHAND ] - Initialize value: {self.inputOrigs}")
            self.handleState  = 1
        pass
    
    def driving(self, signal: list):
        mag = sum([acc**2 for acc in signal[:3]])**0.5
        if signal[-2] > 50:
            self.curState.activate = 0
            self.curState.left     = False
            self.curState.right    = False
            self.curAction.clear()
            return
        if abs(mag - self.acc_avg) > self.threshold:
            self.duplicateStatic = 0 # Is moving
        else:
            self.duplicateStatic = min(STATIC_LIMIT, self.duplicateStatic+1)
        # self.ui.movingCheckBox.setChecked(self.isMoving())
        if self.isMoving():
            self.curAction.append(signal)
        if not self.isMoving():
            self.acc_avg = max(min(self.acc_avg*0.95 + mag*0.05, 1.0), 0.96)
            if len(self.curAction) > 0:
                print(f"[ Action ] - An action data formed!, frame-length={len(self.curAction)}")
                # print(np.array(self.curAction))
                if len(self.curAction) > FRAME_LENGTH_THRESHOLD: # Todo: open another thread for dump file.
                    self.verifyAction() # TODOs
                self.curAction.clear()

    def verifyAction(self):
        # ml
        with torch.no_grad():
            data_array = np.array([self.curAction])
            data_array = data_array.astype(np.float32)
            data_array = torch.from_numpy(data_array)
            
            logits = self.model(torch.FloatTensor(data_array).to(self.device))
            label = logits.argmax(dim=-1).cpu().numpy()
            print(label)

        minAngZ = 90
        maxAngZ = -90
        for frame in self.curAction:
            angZ = frame[-1] - self.inputOrigs[-1]
            minAngZ = min(angZ, minAngZ)
            maxAngZ = max(angZ, maxAngZ)
        if maxAngZ > RIGHTHAND_LIGHT_ANGLE:
            self.curState.left = not self.curState.left
            print("[ RIGHTHAND ] - left light triggered!")
        if minAngZ < -RIGHTHAND_LIGHT_ANGLE:
            print("[ RIGHTHAND ] - right light triggered!")
            self.curState.right =  not self.curState.right       


def main():
    app = QtWidgets.QApplication(sys.argv)
    decisionSender = DecisionSenderBthConn(BioExpG5_2)
    mainControlPanel = MainControlPanel(decisionSender)
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