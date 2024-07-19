from PyQt6 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.main_options = QtWidgets.QWidget(parent=MainWindow)
        self.main_options.setObjectName("main_options")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.main_options)
        self.tabWidget.setGeometry(QtCore.QRect(0, -1, 1280, 721))
        self.tabWidget.setObjectName("tabWidget")
        
        # Settings Tab
        self.settingsTab = QtWidgets.QWidget()
        self.settingsTab.setObjectName("settingsTab")
        
        # Player Icon
        self.playerIcon = QtWidgets.QLabel(parent=self.settingsTab)
        self.playerIcon.setGeometry(QtCore.QRect(50, 50, 200, 200))
        self.playerIcon.setObjectName("playerIcon")
        self.playerIcon.setText("Player Icon")
        self.playerIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.playerIcon.setStyleSheet("border: 2px solid black;")
        
        # Player Info
        self.playerInfo = QtWidgets.QTextEdit(parent=self.settingsTab)
        self.playerInfo.setGeometry(QtCore.QRect(300, 50, 400, 200))
        self.playerInfo.setObjectName("playerInfo")
        self.playerInfo.setReadOnly(True)
        self.playerInfo.setText("Player Information")
        
        # Navigation Buttons
        self.leftButton = QtWidgets.QPushButton(parent=self.settingsTab)
        self.leftButton.setGeometry(QtCore.QRect(50, 300, 100, 50))
        self.leftButton.setObjectName("leftButton")
        self.leftButton.setText("Left")
        
        self.rightButton = QtWidgets.QPushButton(parent=self.settingsTab)
        self.rightButton.setGeometry(QtCore.QRect(200, 300, 100, 50))
        self.rightButton.setObjectName("rightButton")
        self.rightButton.setText("Right")
        
        self.chooseButton = QtWidgets.QPushButton(parent=self.settingsTab)
        self.chooseButton.setGeometry(QtCore.QRect(350, 300, 100, 50))
        self.chooseButton.setObjectName("chooseButton")
        self.chooseButton.setText("Choose")
        
        self.tabWidget.addTab(self.settingsTab, "Settings")
        
        # Keep the second tab as is
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        # ... (rest of the tab_2 code remains the same)
        
        MainWindow.setCentralWidget(self.main_options)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), _translate("MainWindow", "Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))

def options():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    Form.show()
    ui = Ui_MainWindow()
    ui.setupUi(Form)
    sys.exit(app.exec())