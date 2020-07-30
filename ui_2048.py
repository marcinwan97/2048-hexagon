# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButtonNewGame = QPushButton(self.centralwidget)
        self.pushButtonNewGame.setObjectName(u"pushButtonNewGame")
        self.pushButtonNewGame.setGeometry(QRect(860, 60, 81, 41))
        self.pushButtonLeftUp = QPushButton(self.centralwidget)
        self.pushButtonLeftUp.setObjectName(u"pushButtonLeftUp")
        self.pushButtonLeftUp.setGeometry(QRect(860, 320, 90, 40))
        font = QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.pushButtonLeftUp.setFont(font)
        self.pushButtonUp = QPushButton(self.centralwidget)
        self.pushButtonUp.setObjectName(u"pushButtonUp")
        self.pushButtonUp.setGeometry(QRect(970, 270, 90, 40))
        self.pushButtonUp.setFont(font)
        self.pushButtonRightUp = QPushButton(self.centralwidget)
        self.pushButtonRightUp.setObjectName(u"pushButtonRightUp")
        self.pushButtonRightUp.setGeometry(QRect(1080, 320, 90, 40))
        self.pushButtonRightUp.setFont(font)
        self.pushButtonLeftDown = QPushButton(self.centralwidget)
        self.pushButtonLeftDown.setObjectName(u"pushButtonLeftDown")
        self.pushButtonLeftDown.setGeometry(QRect(860, 380, 90, 40))
        self.pushButtonLeftDown.setFont(font)
        self.pushButtonDown = QPushButton(self.centralwidget)
        self.pushButtonDown.setObjectName(u"pushButtonDown")
        self.pushButtonDown.setGeometry(QRect(970, 430, 90, 40))
        self.pushButtonDown.setFont(font)
        self.pushButtonRightDown = QPushButton(self.centralwidget)
        self.pushButtonRightDown.setObjectName(u"pushButtonRightDown")
        self.pushButtonRightDown.setGeometry(QRect(1080, 380, 90, 40))
        self.pushButtonRightDown.setFont(font)
        self.groupBoxBoardSize = QGroupBox(self.centralwidget)
        self.groupBoxBoardSize.setObjectName(u"groupBoxBoardSize")
        self.groupBoxBoardSize.setGeometry(QRect(950, 60, 101, 111))
        self.radioButton5 = QRadioButton(self.groupBoxBoardSize)
        self.radioButton5.setObjectName(u"radioButton5")
        self.radioButton5.setGeometry(QRect(10, 80, 95, 20))
        self.radioButton2 = QRadioButton(self.groupBoxBoardSize)
        self.radioButton2.setObjectName(u"radioButton2")
        self.radioButton2.setGeometry(QRect(10, 20, 95, 20))
        self.radioButton3 = QRadioButton(self.groupBoxBoardSize)
        self.radioButton3.setObjectName(u"radioButton3")
        self.radioButton3.setGeometry(QRect(10, 40, 95, 20))
        self.radioButton3.setChecked(True)
        self.radioButton4 = QRadioButton(self.groupBoxBoardSize)
        self.radioButton4.setObjectName(u"radioButton4")
        self.radioButton4.setGeometry(QRect(10, 60, 95, 20))
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(20, 60, 811, 691))
        self.graphicsView.setFrameShadow(QFrame.Sunken)
        self.hexLabel = QLabel(self.centralwidget)
        self.hexLabel.setObjectName(u"hexLabel")
        self.hexLabel.setGeometry(QRect(950, 310, 131, 121))
        self.label1 = QLabel(self.centralwidget)
        self.label1.setObjectName(u"label1")
        self.label1.setGeometry(QRect(840, 510, 351, 51))
        font1 = QFont()
        font1.setPointSize(16)
        self.label1.setFont(font1)
        self.label2 = QLabel(self.centralwidget)
        self.label2.setObjectName(u"label2")
        self.label2.setGeometry(QRect(840, 580, 351, 51))
        self.label2.setFont(font1)
        self.labelTurn = QLabel(self.centralwidget)
        self.labelTurn.setObjectName(u"labelTurn")
        self.labelTurn.setGeometry(QRect(20, 0, 211, 51))
        self.labelTurn.setFont(font1)
        self.groupBoxGameMode = QGroupBox(self.centralwidget)
        self.groupBoxGameMode.setObjectName(u"groupBoxGameMode")
        self.groupBoxGameMode.setGeometry(QRect(1050, 60, 121, 111))
        self.radioButtonAI = QRadioButton(self.groupBoxGameMode)
        self.radioButtonAI.setObjectName(u"radioButtonAI")
        self.radioButtonAI.setGeometry(QRect(10, 80, 95, 20))
        self.radioButtonSingle = QRadioButton(self.groupBoxGameMode)
        self.radioButtonSingle.setObjectName(u"radioButtonSingle")
        self.radioButtonSingle.setGeometry(QRect(10, 20, 95, 20))
        self.radioButtonSingle.setChecked(True)
        self.radioButtonHotSeat = QRadioButton(self.groupBoxGameMode)
        self.radioButtonHotSeat.setObjectName(u"radioButtonHotSeat")
        self.radioButtonHotSeat.setGeometry(QRect(10, 40, 95, 20))
        self.radioButtonHotSeat.setChecked(False)
        self.radioButtonOnline = QRadioButton(self.groupBoxGameMode)
        self.radioButtonOnline.setObjectName(u"radioButtonOnline")
        self.radioButtonOnline.setGeometry(QRect(10, 60, 95, 20))
        self.lineEditServer = QLineEdit(self.centralwidget)
        self.lineEditServer.setObjectName(u"lineEditServer")
        self.lineEditServer.setGeometry(QRect(1030, 180, 141, 22))
        self.labelServer = QLabel(self.centralwidget)
        self.labelServer.setObjectName(u"labelServer")
        self.labelServer.setGeometry(QRect(900, 180, 131, 20))
        self.labelStatus = QLabel(self.centralwidget)
        self.labelStatus.setObjectName(u"labelStatus")
        self.labelStatus.setGeometry(QRect(430, 0, 431, 51))
        self.labelStatus.setFont(font1)
        self.labelInfo = QLabel(self.centralwidget)
        self.labelInfo.setObjectName(u"labelInfo")
        self.labelInfo.setGeometry(QRect(840, 0, 351, 51))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setKerning(True)
        self.labelInfo.setFont(font2)
        self.pushButtonLoadConfig = QPushButton(self.centralwidget)
        self.pushButtonLoadConfig.setObjectName(u"pushButtonLoadConfig")
        self.pushButtonLoadConfig.setGeometry(QRect(1050, 210, 121, 31))
        self.pushButtonSaveConfig = QPushButton(self.centralwidget)
        self.pushButtonSaveConfig.setObjectName(u"pushButtonSaveConfig")
        self.pushButtonSaveConfig.setGeometry(QRect(920, 210, 121, 31))
        self.pushButtonReplay = QPushButton(self.centralwidget)
        self.pushButtonReplay.setObjectName(u"pushButtonReplay")
        self.pushButtonReplay.setGeometry(QRect(1040, 690, 121, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hexagon 2048 - Marcin Wankiewicz 172118", None))
        self.pushButtonNewGame.setText(QCoreApplication.translate("MainWindow", u"New Game", None))
        self.pushButtonLeftUp.setText(QCoreApplication.translate("MainWindow", u"LEFT-UP", None))
        self.pushButtonUp.setText(QCoreApplication.translate("MainWindow", u"UP", None))
        self.pushButtonRightUp.setText(QCoreApplication.translate("MainWindow", u"RIGHT-UP", None))
        self.pushButtonLeftDown.setText(QCoreApplication.translate("MainWindow", u"LEFT-DOWN", None))
        self.pushButtonDown.setText(QCoreApplication.translate("MainWindow", u"DOWN", None))
        self.pushButtonRightDown.setText(QCoreApplication.translate("MainWindow", u"RIGHT-DOWN", None))
        self.groupBoxBoardSize.setTitle(QCoreApplication.translate("MainWindow", u"Board size:", None))
        self.radioButton5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.radioButton2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.radioButton3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.radioButton4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.hexLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label1.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600; color:#33dc30;\">Player 1 score:</span></p></body></html>", None))
        self.label2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600; color:#aa1900;\">Player 2 score:</span></p></body></html>", None))
        self.labelTurn.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600; color:#33dc30;\">Player 1 turn:</span></p></body></html>", None))
        self.groupBoxGameMode.setTitle(QCoreApplication.translate("MainWindow", u"Game mode", None))
        self.radioButtonAI.setText(QCoreApplication.translate("MainWindow", u"Versus AI", None))
        self.radioButtonSingle.setText(QCoreApplication.translate("MainWindow", u"Singleplayer", None))
        self.radioButtonHotSeat.setText(QCoreApplication.translate("MainWindow", u"Hot seat", None))
        self.radioButtonOnline.setText(QCoreApplication.translate("MainWindow", u"Online", None))
        self.lineEditServer.setText(QCoreApplication.translate("MainWindow", u"localhost", None))
        self.labelServer.setText(QCoreApplication.translate("MainWindow", u"Server IP (for online)", None))
        self.labelStatus.setText(QCoreApplication.translate("MainWindow", u"Waiting for second player...", None))
        self.labelInfo.setText(QCoreApplication.translate("MainWindow", u"Only player 1 can start a new online game!", None))
        self.pushButtonLoadConfig.setText(QCoreApplication.translate("MainWindow", u"Load configuration", None))
        self.pushButtonSaveConfig.setText(QCoreApplication.translate("MainWindow", u"Save configuration", None))
        self.pushButtonReplay.setText(QCoreApplication.translate("MainWindow", u"Replay last game", None))
    # retranslateUi
