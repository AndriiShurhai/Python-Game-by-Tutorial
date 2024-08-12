import sys
from PyQt6 import QtCore, QtGui, QtWidgets

class CurrentPlayer:
    def __init__(self, name, square_icon_path, vertical_icon_path, info):
        self.name = name
        self.square_icon_path = square_icon_path
        self.vertical_icon_path = vertical_icon_path
        self.info = info

class SettingsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Title of the section
        self.sectionTitle = QtWidgets.QLabel("Character Settings")
        self.sectionTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sectionTitle.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 20px;
        """)
        self.layout.addWidget(self.sectionTitle)

        # Content layout
        self.contentLayout = QtWidgets.QHBoxLayout()
        self.contentLayout.setSpacing(30)
        self.layout.addLayout(self.contentLayout)

        # Left column: Character Name and Player Icons
        self.leftColumnLayout = QtWidgets.QVBoxLayout()
        self.leftColumnLayout.setSpacing(20)
        self.contentLayout.addLayout(self.leftColumnLayout)

        # Character name
        self.characterName = QtWidgets.QLabel("Current Character: Unknown")
        self.characterName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.characterName.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #2A2A2A;
            padding: 10px;
            border-radius: 5px;
        """)
        self.leftColumnLayout.addWidget(self.characterName)

        # Square Player Icon
        self.squarePlayerIcon = QtWidgets.QLabel()
        self.squarePlayerIcon.setFixedSize(200, 200)
        self.squarePlayerIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.squarePlayerIcon.setStyleSheet("""
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            background-color: #2A2A2A;
            color: #FFFFFF;
        """)
        self.squarePlayerIcon.setText("Square Player Icon")
        self.leftColumnLayout.addWidget(self.squarePlayerIcon)

        # Vertical Player Icon
        self.verticalPlayerIcon = QtWidgets.QLabel()
        self.verticalPlayerIcon.setFixedSize(200, 300)
        self.verticalPlayerIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalPlayerIcon.setStyleSheet("""
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            background-color: #2A2A2A;
            color: #FFFFFF;
        """)
        self.verticalPlayerIcon.setText("Vertical Player Icon")
        self.leftColumnLayout.addWidget(self.verticalPlayerIcon)

        # Add stretch to push everything to the top
        self.leftColumnLayout.addStretch()

        # Right column: Player Info and Buttons
        self.rightColumnLayout = QtWidgets.QVBoxLayout()
        self.rightColumnLayout.setSpacing(20)
        self.contentLayout.addLayout(self.rightColumnLayout)

        # Player Info
        self.playerInfo = QtWidgets.QTextEdit()
        self.playerInfo.setReadOnly(True)
        self.playerInfo.setText("Player Information")
        self.playerInfo.setFixedHeight(520)
        self.playerInfo.setStyleSheet("""
            background-color: #2A2A2A;
            color: #FFFFFF;
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        """)
        self.rightColumnLayout.addWidget(self.playerInfo)

        # Navigation Buttons
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        button_style = """
            QPushButton {
                background-color: #3A3A3A;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4A4A4A;
            }
            QPushButton:pressed {
                background-color: #2A2A2A;
            }
        """
        self.leftButton = QtWidgets.QPushButton("Left")
        self.rightButton = QtWidgets.QPushButton("Right")
        self.chooseButton = QtWidgets.QPushButton("Choose")
        
        for button in [self.leftButton, self.rightButton, self.chooseButton]:
            button.setStyleSheet(button_style)
            self.buttonLayout.addWidget(button)

        self.rightColumnLayout.addLayout(self.buttonLayout)

        # Add stretch to push everything to the top
        self.rightColumnLayout.addStretch()

class AudioTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QtWidgets.QLabel("Audio Settings")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        # Main volume control
        volume_label = QtWidgets.QLabel("Volume:")
        volume_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        layout.addWidget(volume_label)
        layout.addWidget(volume_slider)

        # Checkboxes for audio control
        checkbox_style = """
            QCheckBox {
                color: #FFFFFF;
                font-size: 16px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #999999;
                background: #2A2A2A;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #3A3A3A;
                background: #4A90E2;
            }
        """

        self.main_menu_music_cb = QtWidgets.QCheckBox("Enable Main Menu Music")
        self.main_menu_music_cb.setStyleSheet(checkbox_style)
        layout.addWidget(self.main_menu_music_cb)

        self.game_music_cb = QtWidgets.QCheckBox("Enable Game Music")
        self.game_music_cb.setStyleSheet(checkbox_style)
        layout.addWidget(self.game_music_cb)

        self.game_sounds_cb = QtWidgets.QCheckBox("Enable Game Sounds")
        self.game_sounds_cb.setStyleSheet(checkbox_style)
        layout.addWidget(self.game_sounds_cb)

        # Connect checkboxes to functions
        self.main_menu_music_cb.stateChanged.connect(self.toggle_main_menu_music)
        self.game_music_cb.stateChanged.connect(self.toggle_game_music)
        self.game_sounds_cb.stateChanged.connect(self.toggle_game_sounds)

        # Add stretch to push everything to the top
        layout.addStretch()

    def toggle_main_menu_music(self, state):
        # Implement the logic to enable/disable main menu music
        print(f"Main menu music {'enabled' if state == QtCore.Qt.CheckState.Checked else 'disabled'}")

    def toggle_game_music(self, state):
        # Implement the logic to enable/disable game music
        print(f"Game music {'enabled' if state == QtCore.Qt.CheckState.Checked else 'disabled'}")

    def toggle_game_sounds(self, state):
        # Implement the logic to enable/disable game sounds
        print(f"Game sounds {'enabled' if state == QtCore.Qt.CheckState.Checked else 'disabled'}")

class MovementGuideTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QtWidgets.QLabel("Movement Guide")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        guide_text = QtWidgets.QTextEdit()
        guide_text.setReadOnly(True)
        guide_text.setStyleSheet("""
            background-color: #2A2A2A;
            color: #FFFFFF;
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        """)
        guide_text.setText("Add your movement guide information here.")
        layout.addWidget(guide_text)

class InfoTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QtWidgets.QLabel("Information")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        info_text = QtWidgets.QTextEdit()
        info_text.setReadOnly(True)
        info_text.setStyleSheet("""
            background-color: #2A2A2A;
            color: #FFFFFF;
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        """)
        info_text.setText("Add your game information here.")
        layout.addWidget(info_text)

class CreditsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QtWidgets.QLabel("Credits")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        credits_text = QtWidgets.QTextEdit()
        credits_text.setReadOnly(True)
        credits_text.setStyleSheet("""
            background-color: #2A2A2A;
            color: #FFFFFF;
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        """)
        credits_text.setText("Add your credits information here.")
        layout.addWidget(credits_text)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, WINDOW_WIDTH, WINDOW_HEIGHT):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.main_options = QtWidgets.QWidget(parent=MainWindow)
        self.main_options.setObjectName("main_options")
        

        # Set the application style
        QtWidgets.QApplication.setStyle("Fusion")

        # Set a pleasing color palette
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
        palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ColorRole.ToolTipBase, QtCore.Qt.GlobalColor.white)
        palette.setColor(QtGui.QPalette.ColorRole.ToolTipText, QtCore.Qt.GlobalColor.white)
        palette.setColor(QtGui.QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.white)
        palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.white)
        palette.setColor(QtGui.QPalette.ColorRole.BrightText, QtCore.Qt.GlobalColor.red)
        palette.setColor(QtGui.QPalette.ColorRole.Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.black)
        QtWidgets.QApplication.setPalette(palette)

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self.main_options)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(parent=self.main_options)
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #3A3A3A; }
            QTabBar::tab { 
                background-color: #2A2A2A; 
                color: white;
                padding: 10px 15px;
                border: 1px solid #3A3A3A;
            }
            QTabBar::tab:selected { 
                background-color: #3A3A3A;
                border-bottom-color: #3A3A3A;
            }
        """)
        self.main_layout.addWidget(self.tabWidget)

        # Add tabs
        self.settingsTab = SettingsTab()
        self.audioTab = AudioTab()
        self.movementGuideTab = MovementGuideTab()
        self.infoTab = InfoTab()
        self.creditsTab = CreditsTab()

        self.tabWidget.addTab(self.settingsTab, "Settings")
        self.tabWidget.addTab(self.audioTab, "Audio")
        self.tabWidget.addTab(self.movementGuideTab, "Movement Guide")
        self.tabWidget.addTab(self.infoTab, "Info")
        self.tabWidget.addTab(self.creditsTab, "Credits")

        # Set central widget
        MainWindow.setCentralWidget(self.main_options)

        # Menu and status bar
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, WINDOW_WIDTH, 22))
        self.menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2A2A2A;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #3A3A3A;
            }
        """)
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setStyleSheet("background-color: #2A2A2A; color: white;")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect buttons to functions
        self.settingsTab.leftButton.clicked.connect(self.previous_player)
        self.settingsTab.rightButton.clicked.connect(self.next_player)
        self.settingsTab.chooseButton.clicked.connect(self.choose_player)

        # Initialize player data
        self.players = [
            CurrentPlayer("Андрійко", "path/to/square1.png", "path/to/vertical1.png", "Info about Player 1"),
            CurrentPlayer("Player 2", "path/to/square2.png", "path/to/vertical2.png", "Info about Player 2"),
            CurrentPlayer("Player 3", "path/to/square3.png", "path/to/vertical3.png", "Info about Player 3"),
        ]
        self.current_player_index = 0

        # Display initial player
        self.update_player_display()
        
    def update_player_display(self):
        player = self.players[self.current_player_index]
        
        # Update character name
        self.settingsTab.characterName.setText(f"Current Character: {player.name}")
        
        # Update square icon
        square_pixmap = QtGui.QPixmap(player.square_icon_path)
        self.settingsTab.squarePlayerIcon.setPixmap(square_pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
        # Update vertical icon
        vertical_pixmap = QtGui.QPixmap(player.vertical_icon_path)
        self.settingsTab.verticalPlayerIcon.setPixmap(vertical_pixmap.scaled(200, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
        # Update player info
        self.settingsTab.playerInfo.setText(player.info)

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.update_player_display()

    def previous_player(self):
        self.current_player_index = (self.current_player_index - 1) % len(self.players)
        self.update_player_display()

    def choose_player(self):
        player = self.players[self.current_player_index]
        QtWidgets.QMessageBox.information(None, "Player Chosen", f"You have chosen {player.name}!")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Game Options"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), _translate("MainWindow", "Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.audioTab), _translate("MainWindow", "Audio"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.movementGuideTab), _translate("MainWindow", "Movement Guide"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.infoTab), _translate("MainWindow", "Info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.creditsTab), _translate("MainWindow", "Credits"))



def options(WINDOW_WIDTH, WINDOW_HEIGHT):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, WINDOW_WIDTH, WINDOW_HEIGHT)
    MainWindow.show()
    sys.exit(app.exec())
