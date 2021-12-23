# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controlPanel.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(553, 531)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.controlLabel = QtWidgets.QLabel(self.centralwidget)
        self.controlLabel.setGeometry(QtCore.QRect(130, 180, 91, 31))
        self.controlLabel.setObjectName("controlLabel")
        self.directionSlider = QtWidgets.QSlider(self.centralwidget)
        self.directionSlider.setGeometry(QtCore.QRect(60, 280, 181, 16))
        self.directionSlider.setMinimum(-5)
        self.directionSlider.setMaximum(5)
        self.directionSlider.setProperty("value", 0)
        self.directionSlider.setOrientation(QtCore.Qt.Horizontal)
        self.directionSlider.setObjectName("directionSlider")
        self.speedSlider = QtWidgets.QSlider(self.centralwidget)
        self.speedSlider.setGeometry(QtCore.QRect(140, 220, 16, 160))
        self.speedSlider.setMinimum(-5)
        self.speedSlider.setMaximum(5)
        self.speedSlider.setProperty("value", -5)
        self.speedSlider.setOrientation(QtCore.Qt.Vertical)
        self.speedSlider.setObjectName("speedSlider")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(330, 265, 171, 31))
        self.checkBox.setObjectName("checkBox")
        self.speedLabel = QtWidgets.QLabel(self.centralwidget)
        self.speedLabel.setGeometry(QtCore.QRect(160, 340, 47, 31))
        self.speedLabel.setObjectName("speedLabel")
        self.directionLabel = QtWidgets.QLabel(self.centralwidget)
        self.directionLabel.setGeometry(QtCore.QRect(60, 250, 31, 31))
        self.directionLabel.setObjectName("directionLabel")
        self.leftPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.leftPushButton.setGeometry(QtCore.QRect(270, 312, 75, 31))
        self.leftPushButton.setCheckable(True)
        self.leftPushButton.setObjectName("leftPushButton")
        self.rightPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.rightPushButton.setGeometry(QtCore.QRect(370, 312, 75, 31))
        self.rightPushButton.setCheckable(True)
        self.rightPushButton.setObjectName("rightPushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 553, 22))
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
        self.controlLabel.setText(_translate("MainWindow", "Control"))
        self.checkBox.setText(_translate("MainWindow", "Activated"))
        self.speedLabel.setText(_translate("MainWindow", "-5"))
        self.directionLabel.setText(_translate("MainWindow", "0"))
        self.leftPushButton.setText(_translate("MainWindow", "LEFT"))
        self.rightPushButton.setText(_translate("MainWindow", "RIGHT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())