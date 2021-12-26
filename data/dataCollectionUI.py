# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dataCollection.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(290, 80, 20, 651))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.signalRcvLabel = QtWidgets.QLabel(self.centralwidget)
        self.signalRcvLabel.setGeometry(QtCore.QRect(100, 70, 171, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.signalRcvLabel.setFont(font)
        self.signalRcvLabel.setObjectName("signalRcvLabel")
        self.accXLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.accXLineEdit.setEnabled(False)
        self.accXLineEdit.setGeometry(QtCore.QRect(210, 140, 61, 31))
        self.accXLineEdit.setObjectName("accXLineEdit")
        self.accXLabel = QtWidgets.QLabel(self.centralwidget)
        self.accXLabel.setGeometry(QtCore.QRect(90, 140, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.accXLabel.setFont(font)
        self.accXLabel.setObjectName("accXLabel")
        self.accYLabel = QtWidgets.QLabel(self.centralwidget)
        self.accYLabel.setGeometry(QtCore.QRect(90, 190, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.accYLabel.setFont(font)
        self.accYLabel.setObjectName("accYLabel")
        self.accYLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.accYLineEdit.setEnabled(False)
        self.accYLineEdit.setGeometry(QtCore.QRect(210, 190, 61, 31))
        self.accYLineEdit.setText("")
        self.accYLineEdit.setObjectName("accYLineEdit")
        self.accZLabel = QtWidgets.QLabel(self.centralwidget)
        self.accZLabel.setGeometry(QtCore.QRect(90, 240, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.accZLabel.setFont(font)
        self.accZLabel.setObjectName("accZLabel")
        self.accZLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.accZLineEdit.setEnabled(False)
        self.accZLineEdit.setGeometry(QtCore.QRect(210, 240, 61, 31))
        self.accZLineEdit.setText("")
        self.accZLineEdit.setObjectName("accZLineEdit")
        self.angXLabel = QtWidgets.QLabel(self.centralwidget)
        self.angXLabel.setGeometry(QtCore.QRect(90, 310, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.angXLabel.setFont(font)
        self.angXLabel.setObjectName("angXLabel")
        self.angXLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.angXLineEdit.setEnabled(False)
        self.angXLineEdit.setGeometry(QtCore.QRect(210, 310, 61, 31))
        self.angXLineEdit.setObjectName("angXLineEdit")
        self.angYLabel = QtWidgets.QLabel(self.centralwidget)
        self.angYLabel.setGeometry(QtCore.QRect(90, 360, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.angYLabel.setFont(font)
        self.angYLabel.setObjectName("angYLabel")
        self.angYLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.angYLineEdit.setEnabled(False)
        self.angYLineEdit.setGeometry(QtCore.QRect(210, 360, 61, 31))
        self.angYLineEdit.setText("")
        self.angYLineEdit.setObjectName("angYLineEdit")
        self.angZLabel = QtWidgets.QLabel(self.centralwidget)
        self.angZLabel.setGeometry(QtCore.QRect(90, 410, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.angZLabel.setFont(font)
        self.angZLabel.setObjectName("angZLabel")
        self.angZLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.angZLineEdit.setEnabled(False)
        self.angZLineEdit.setGeometry(QtCore.QRect(210, 410, 61, 31))
        self.angZLineEdit.setText("")
        self.angZLineEdit.setObjectName("angZLineEdit")
        self.dataCollectionLabel = QtWidgets.QLabel(self.centralwidget)
        self.dataCollectionLabel.setGeometry(QtCore.QRect(340, 70, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.dataCollectionLabel.setFont(font)
        self.dataCollectionLabel.setObjectName("dataCollectionLabel")
        self.movingCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.movingCheckBox.setEnabled(False)
        self.movingCheckBox.setGeometry(QtCore.QRect(340, 150, 141, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.movingCheckBox.setFont(font)
        self.movingCheckBox.setIconSize(QtCore.QSize(32, 32))
        self.movingCheckBox.setObjectName("movingCheckBox")
        self.thresholdLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.thresholdLineEdit.setGeometry(QtCore.QRect(780, 180, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.thresholdLineEdit.setFont(font)
        self.thresholdLineEdit.setObjectName("thresholdLineEdit")
        self.thresholdLabel = QtWidgets.QLabel(self.centralwidget)
        self.thresholdLabel.setGeometry(QtCore.QRect(520, 170, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.thresholdLabel.setFont(font)
        self.thresholdLabel.setObjectName("thresholdLabel")
        self.sigRcvConnCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.sigRcvConnCheckBox.setEnabled(False)
        self.sigRcvConnCheckBox.setGeometry(QtCore.QRect(100, 610, 181, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.sigRcvConnCheckBox.setFont(font)
        self.sigRcvConnCheckBox.setObjectName("sigRcvConnCheckBox")
        self.magLabel = QtWidgets.QLabel(self.centralwidget)
        self.magLabel.setGeometry(QtCore.QRect(90, 520, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.magLabel.setFont(font)
        self.magLabel.setObjectName("magLabel")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(110, 480, 151, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.magLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.magLineEdit.setEnabled(False)
        self.magLineEdit.setGeometry(QtCore.QRect(210, 520, 61, 31))
        self.magLineEdit.setText("")
        self.magLineEdit.setObjectName("magLineEdit")
        self.thresholdPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.thresholdPushButton.setGeometry(QtCore.QRect(910, 180, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.thresholdPushButton.setFont(font)
        self.thresholdPushButton.setObjectName("thresholdPushButton")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(327, 260, 731, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.isRecordingPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.isRecordingPushButton.setGeometry(QtCore.QRect(340, 332, 141, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.isRecordingPushButton.setFont(font)
        self.isRecordingPushButton.setCheckable(True)
        self.isRecordingPushButton.setObjectName("isRecordingPushButton")
        self.classNameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.classNameLineEdit.setGeometry(QtCore.QRect(780, 350, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.classNameLineEdit.setFont(font)
        self.classNameLineEdit.setObjectName("classNameLineEdit")
        self.classNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.classNameLabel.setGeometry(QtCore.QRect(520, 340, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.classNameLabel.setFont(font)
        self.classNameLabel.setObjectName("classNameLabel")
        self.classNamePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.classNamePushButton.setGeometry(QtCore.QRect(910, 350, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.classNamePushButton.setFont(font)
        self.classNamePushButton.setObjectName("classNamePushButton")
        self.dumpDataPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.dumpDataPushButton.setGeometry(QtCore.QRect(340, 510, 651, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.dumpDataPushButton.setFont(font)
        self.dumpDataPushButton.setCheckable(False)
        self.dumpDataPushButton.setObjectName("dumpDataPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.signalRcvLabel.setText(_translate("MainWindow", "SignalRcv"))
        self.accXLabel.setText(_translate("MainWindow", "AccX: "))
        self.accYLabel.setText(_translate("MainWindow", "AccY: "))
        self.accZLabel.setText(_translate("MainWindow", "AccZ: "))
        self.angXLabel.setText(_translate("MainWindow", "AngX: "))
        self.angYLabel.setText(_translate("MainWindow", "AngY: "))
        self.angZLabel.setText(_translate("MainWindow", "AngZ: "))
        self.dataCollectionLabel.setText(_translate("MainWindow", "Data Collection"))
        self.movingCheckBox.setText(_translate("MainWindow", "Moving"))
        self.thresholdLabel.setText(_translate("MainWindow", "Threshold: "))
        self.sigRcvConnCheckBox.setText(_translate("MainWindow", "Connected"))
        self.magLabel.setText(_translate("MainWindow", "Mag:"))
        self.thresholdPushButton.setText(_translate("MainWindow", "SET"))
        self.isRecordingPushButton.setText(_translate("MainWindow", "Is Recording"))
        self.classNameLabel.setText(_translate("MainWindow", "Class Name: "))
        self.classNamePushButton.setText(_translate("MainWindow", "SET"))
        self.dumpDataPushButton.setText(_translate("MainWindow", "Dump Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
