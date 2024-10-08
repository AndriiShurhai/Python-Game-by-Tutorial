import sys
import json
import os
from os.path import join
from support import import_image,  import_folder
from PyQt6 import QtCore, QtGui, QtWidgets
import pygame

class Enemy:
    def __init__(self, name, image_path, animation_path, info):
        self.name = name
        self.image_path = image_path
        self.animation_path = animation_path
        self.info = info
        self.frames = []
        self.frame_index = 0
        self.animation_speed = 5
        self.load_animation_frames()

    def load_animation_frames(self):
        if len(self.animation_path) >= 40:
            animation_files = sorted([f for f in os.listdir(self.animation_path) if f.endswith(('.png', '.jpg', '.gif'))])
            for frame_file in animation_files:
                frame_path = os.path.join(self.animation_path, frame_file)
                self.frames.append(QtGui.QPixmap(frame_path))

class EnemiesTab(QtWidgets.QWidget):
    def __init__(self, enemies, parent=None):
        super().__init__(parent)
        self.enemies = enemies
        self.current_enemy_index = 0
        self.setupUi()
        self.last_update_time = QtCore.QTime.currentTime()
        self.animation_timer = QtCore.QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)  # ~60 FPS

    def setupUi(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Title of the section
        self.sectionTitle = QtWidgets.QLabel("Enemy Settings")
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

        # Left column: Enemy Name, Image Icon, and Animation Icon
        self.leftColumnLayout = QtWidgets.QVBoxLayout()
        self.leftColumnLayout.setSpacing(40)
        self.contentLayout.addLayout(self.leftColumnLayout)

        # Enemy name
        self.enemyName = QtWidgets.QLabel("Current Enemy: Unknown")
        self.enemyName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.enemyName.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #2A2A2A;
            padding: 10px;
            border-radius: 5px;
        """)
        self.leftColumnLayout.addWidget(self.enemyName)

        # Enemy Image Icon
        self.enemyImageIcon = QtWidgets.QLabel()
        self.enemyImageIcon.setFixedSize(200, 200)
        self.enemyImageIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.enemyImageIcon.setStyleSheet("""
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            background-color: #2A2A2A;
            color: #FFFFFF;
        """)
        self.enemyImageIcon.setText("Enemy Image")
        self.leftColumnLayout.addWidget(self.enemyImageIcon)

        # Enemy Animation Icon
        self.enemyAnimationIcon = QtWidgets.QLabel()
        self.enemyAnimationIcon.setFixedSize(200, 200)
        self.enemyAnimationIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.enemyAnimationIcon.setStyleSheet("""
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            background-color: #2A2A2A;
            color: #FFFFFF;
        """)
        self.enemyAnimationIcon.setText("Enemy Animation")
        self.leftColumnLayout.addWidget(self.enemyAnimationIcon)

        # Add stretch to push everything to the top
        self.leftColumnLayout.addStretch()

        # Right column: Enemy Info, Video Guide, and Buttons
        self.rightColumnLayout = QtWidgets.QVBoxLayout()
        self.rightColumnLayout.setSpacing(20)
        self.contentLayout.addLayout(self.rightColumnLayout)

        # Enemy Info
        self.enemyInfo = QtWidgets.QTextEdit()
        self.enemyInfo.setReadOnly(True)
        self.enemyInfo.setText("Enemy Information")
        self.enemyInfo.setStyleSheet("""
            background-color: #2A2A2A;
            color: #FFFFFF;
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        """)
        self.rightColumnLayout.addWidget(self.enemyInfo)

        self.videoGuideStyle = """
            border: 2px solid #3A3A3A;
            border-radius: 10px;
            background-color: #2A2A2A;
            color: #FFFFFF;
        """
        self.videoGuidesLayout = QtWidgets.QHBoxLayout()
        self.videoGuidesLayout.setSpacing(20)
        self.videoGuide = QtWidgets.QLabel("Video Guide Placeholder")
        self.damageVideoGuide = QtWidgets.QLabel("Video Guide Placeholder")
        self.killingVideoGuide = QtWidgets.QLabel("Video Guide Placeholder")

        for videoGuide in [self.videoGuide, self.damageVideoGuide, self.killingVideoGuide]:
            videoGuide.setFixedSize(300, 200)
            videoGuide.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            videoGuide.setStyleSheet(self.videoGuideStyle)
            self.videoGuidesLayout.addWidget(videoGuide)

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
        self.leftButton = QtWidgets.QPushButton("Previous")
        self.rightButton = QtWidgets.QPushButton("Next")
        
        for button in [self.leftButton, self.rightButton]:
            button.setStyleSheet(button_style)
            self.buttonLayout.addWidget(button)

        self.rightColumnLayout.addLayout(self.videoGuidesLayout)
        self.rightColumnLayout.addLayout(self.buttonLayout)


        # Connect buttons to functions
        self.leftButton.clicked.connect(self.previous_enemy)
        self.rightButton.clicked.connect(self.next_enemy)

        # Display initial enemy
        self.update_enemy_display()

    def update_enemy_display(self):
        enemy = self.enemies[self.current_enemy_index]
        
        # Update enemy name
        self.enemyName.setText(f"Current Enemy: {enemy.name}")
        
        # Update image icon
        image_pixmap = QtGui.QPixmap(enemy.image_path)
        self.enemyImageIcon.setPixmap(image_pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
        # Update animation icon
        animation_pixmap = QtGui.QPixmap(enemy.animation_path)
        self.enemyAnimationIcon.setPixmap(animation_pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
        # Update enemy info
        self.enemyInfo.setText(enemy.info)
        
        # Update video guide placeholder
        self.videoGuide.setText(f"Video Guide for {enemy.name}")
        self.damageVideoGuide.setText(f"Video Guide for {enemy.name}")
        self.killingVideoGuide.setText(f"Video Guide for {enemy.name}")

    def update_animation(self):
        current_time = QtCore.QTime.currentTime()
        delta_time = self.last_update_time.msecsTo(current_time) / 1000.0
        self.last_update_time = current_time

        enemy = self.enemies[self.current_enemy_index]
        if enemy.frames:
            enemy.frame_index += enemy.animation_speed * delta_time
            frame_index = int(enemy.frame_index % len(enemy.frames))
            current_frame = enemy.frames[frame_index]
            self.enemyAnimationIcon.setPixmap(current_frame.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.enemyAnimationIcon.setText("No Animation Available")

    def next_enemy(self):
        self.current_enemy_index = (self.current_enemy_index + 1) % len(self.enemies)
        self.update_enemy_display()

    def previous_enemy(self):
        self.current_enemy_index = (self.current_enemy_index - 1) % len(self.enemies)
        self.update_enemy_display()

class CurrentPlayer:
    def __init__(self, name, square_icon_path, vertical_icon_path, info):
        self.name = name
        self.square_icon_path = square_icon_path
        self.vertical_icon_path = vertical_icon_path
        self.info = info

class SettingsTab(QtWidgets.QWidget):
    def __init__(self, players, parent=None):
        super().__init__(parent)
        self.players = players
        self.current_player_index = 0
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

        # Connect buttons to functions
        self.leftButton.clicked.connect(self.previous_player)
        self.rightButton.clicked.connect(self.next_player)
        self.chooseButton.clicked.connect(self.choose_player)

        # Display initial player
        self.update_player_display()

    def update_player_display(self):
        player = self.players[self.current_player_index]
        
        # Update character name
        self.characterName.setText(f"Current Character: {player.name}")
        
        # Update square icon
        square_pixmap = QtGui.QPixmap(player.square_icon_path)
        self.squarePlayerIcon.setPixmap(square_pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
        # Update vertical icon
        vertical_pixmap = QtGui.QPixmap(player.vertical_icon_path)
        self.verticalPlayerIcon.setPixmap(vertical_pixmap.scaled(200, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        
        # Update player info
        self.playerInfo.setText(player.info)

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.update_player_display()

    def previous_player(self):
        self.current_player_index = (self.current_player_index - 1) % len(self.players)
        self.update_player_display()

    def choose_player(self):
        player = self.players[self.current_player_index]
        QtWidgets.QMessageBox.information(None, "Player Chosen", f"You have chosen {player.name}!")

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
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        layout.addWidget(volume_label)
        layout.addWidget(self.volume_slider)

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

        self.main_menu_music_cb.setChecked(True)
        self.game_music_cb.setChecked(True)
        self.game_sounds_cb.setChecked(True)

        # Connect checkboxes to functions
        self.main_menu_music_cb.stateChanged.connect(self.toggle_main_menu_music)
        self.game_music_cb.stateChanged.connect(self.toggle_game_music)
        self.game_sounds_cb.stateChanged.connect(self.toggle_game_sounds)

        # Add stretch to push everything to the top
        layout.addStretch()

        # Volume control
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.adjust_volume)

        # Balance control
        balance_label = QtWidgets.QLabel("Balance:")
        self.balance_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.balance_slider.setRange(-50, 50)
        self.balance_slider.setValue(0)
        self.balance_slider.valueChanged.connect(self.adjust_balance)
        layout.addWidget(balance_label)
        layout.addWidget(self.balance_slider)

        # Reset button
        reset_button = QtWidgets.QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_button)

        # Set tooltips
        self.volume_slider.setToolTip("Adjust the overall volume")
        self.balance_slider.setToolTip("Adjust the left-right balance")
        self.main_menu_music_cb.setToolTip("Toggle music in the main menu")
        self.game_music_cb.setToolTip("Toggle music during gameplay")
        self.game_sounds_cb.setToolTip("Toggle sound effects during gameplay")

        self.load_config()

    def adjust_volume(self, value):
        print(f"Volume adjusted to {value}%")
        # Implement actual volume adjustment here
        self.save_config()
        self.load_config()


    def adjust_balance(self, value):
        print(f"Balance adjusted to {value}")
        # Implement actual balance adjustment here
        self.save_config()
        self.load_config()

    def reset_to_default(self):
        self.volume_slider.setValue(50)
        self.balance_slider.setValue(0)
        self.main_menu_music_cb.setChecked(True)
        self.game_music_cb.setChecked(True)
        self.game_sounds_cb.setChecked(True)
        self.save_config()
        self.load_config()

    def load_config(self):
        try:
            with open('audio_config.json', 'r') as f:
                config = json.load(f)
            self.volume_slider.setValue(config['volume'])
            self.balance_slider.setValue(config['balance'])
            self.main_menu_music_cb.setChecked(config['main_menu_music'])
            self.game_music_cb.setChecked(config['game_music'])
            self.game_sounds_cb.setChecked(config['game_sounds'])
        except FileNotFoundError:
            print("Config file not found. Using default settings.")

    def save_config(self):
        config = {
            'volume': self.volume_slider.value(),
            'balance': self.balance_slider.value(),
            'main_menu_music': self.main_menu_music_cb.isChecked(),
            'game_music': self.game_music_cb.isChecked(),
            'game_sounds': self.game_sounds_cb.isChecked()
        }
        with open('audio_config.json', 'w') as f:
            json.dump(config, f)

    def toggle_main_menu_music(self, state):
        # Implement the logic to enable/disable main menu music
        print(f"Main menu music {'enabled' if state == QtCore.Qt.CheckState.Checked else 'disabled'}")
        self.save_config()
        self.load_config()

    def toggle_game_music(self, state):
        # Implement the logic to enable/disable game music
        print(f"Game music {'enabled' if state == QtCore.Qt.CheckState.Checked else 'disabled'}")
        self.save_config()
        self.load_config()

    def toggle_game_sounds(self, state):
        # Implement the logic to enable/disable game sounds
        print(f"Game sounds {'enabled' if state == QtCore.Qt.CheckState.Checked else 'disabled'}")
        self.save_config()
        self.load_config()

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

        # Initialize player data
        self.informations = {
            "Andriiko": """Андрійко — один із двох сміливих протагоністів першої частини. Після того, як він ледве вибрався з минулої пригоди, замість того щоб трохи перепочити, Андрійко, як завжди, вляпався в нові проблеми. Він має природний талант знаходити пригоди на свою голову — чи то випадково наступив на скарб, захований під носом у злого пірата, чи то забув здати лабораторну з вишмату. З його невгамовною вдачею, здається, що пригоди самі бігають за ним, як за старим другом. Він один із тих, кого можна назвати "звичайним піратом".""",
            "Flovnes": """Flovnes, Vlad, ZZZZZ. У нього багато імен. Це старий морський вовк, про якого навіть акули розповідають легенди, коли збираються на свої підводні вечірки. Кажуть, що Flovnes був настільки стародавнім піратом, що його перша борода почала сивіти ще до того, як океани на Землі наповнились водою! Озброєний таємничою іржавою шаблею, яка більше схожа на металобрухт, він називав цю зброю Rust і використовував її з такою майстерністю, що навіть інші пірати питали: "А чому це досі не розвалилось?" Але справжній страх наводив Flovnes, коли випускав лазери з очей. Місцеві рибалки навіть розповідають, що бачили, як його лазери підсмажували рибу просто у воді — така собі морська вечеря на швидку руку. Коли цей старий пірат не зайнятий підсмажуванням риби лазерами чи новими піратськими пригодами, він з насолодою вмикає свій ноутбук і грає в Dota 2. Хоч ніхто не впевнений, що з цього правда, Flovnes знову повернувся, щоби зірвати пенсіонерський капелюх і вплутатися в нові піратські пригоди. Хто знає, можливо, наступною його ціллю буде здобути золото стародавніх морських божеств чи просто знайти ідеальний пляжний крісло""",
            "Watashiva Kramar": """Крамер - колоритна фігура у світі фінансів, чия харизма та ексцентричність не знають меж. Цей велетенський чоловік з очима, що світяться азартом, давно став легендою Уолл-стріт. Його гучний сміх можна почути ще до того, як він з'явиться у полі зору, а яскраві краватки з принтами аніме-персонажів стали його фірмовою ознакою.Відомий своєю надзвичайною інтуїцією та схильністю до ризикованих, але прибуткових інвестицій, Крамер довгий час був королем "даху Барвінка" - жаргонна назва специфічного сегменту фондового ринку. Його блискучі операції з акціями принесли йому статус гуру серед молодих інвесторів та шалені статки. Однак, коли прибутковість його улюбленого сектору почала падати, Крамер не розгубився. Замість того, щоб дотримуватися традиційних шляхів, він вирішив зануритися у світ, про який завжди мріяв - світ піратських пригод. Тепер його можна побачити на розкішній яхті "Місяче САлО", названій на честь улюбленого аніме, як він розробляє стратегії для пошуку затонулих скарбів та фінансування експедицій до загублених островів.""",
            "Vasilko": """Василько — один із двох сміливих протагоністів першої частини і справжнє втілення класичного пірата. Здавалося б, він зійшов прямо зі сторінок старих піратських романів, де у кожного героя на поясі висить шабля, а в голові — мрії про заховані скарби. Василько має все, що потрібно справжньому пірату: дерев'яну ногу (на щастя, справжня на місці, але під час бою Василько завжди тримає запасну), папугу, який ніколи не мовчить, і безліч історій про свої «величні» морські подвиги. Але не дайте себе обманути його класичним образом — Василько вміє не тільки хвацько розмахувати шаблею, але й знайти скарб там, де його навіть не мали б заховати. Він настільки звик до піратського життя, що його кожен день починається з того, що він кричить «Йо-хо-хо!» у дзеркало, наче це його ранковий ритуал.""",
            "Levchenko":"""Капітан Левченко "Лего-Мозок" - Це морський вовк який має унікальну суперсилу - перетворювати будь-який непотріб на борту в неймовірні винаходи з Лего. Його каюта більше нагадує майстерню божевільного винахідника, де з конструктора народжуються механічні папуги, що розмовляють, гарматні ядра з пропелерами та навіть підводний човен для втечі від акул.Коли Левченко не зайнятий своїми геніальними винаходами, він з головою поринає у віртуальні битви. Його можна побачити, як він люто тицяє пальцем у екран свого смартфона, намагаючись здобути чергову перемогу в Clash Royale. Горе тому нещасному члену команди, який насмілиться перервати капітана під час його ігрової сесії! Особливо якщо в цей момент якийсь "нікчемний гриб" (як він їх називає) зруйнував його ідеальну стратегію.Левченко щиро вірить, що він - найбагатший пірат в історії. Щоправда, його "скарби" складаються з величезної колекції фігурок з Лего, віртуальних монет у Kingdom Rush та кількох засмальцьованих купюр невідомої валюти. Але хто насмілиться сказати капітану, що його "мільйони" існують лише в його уяві?""",
            "Tooth": """Цей кругленький зубастик не може визначитися, куди ж йому подітися, тому постійно снує туди-сюди, наче маятник на старовинному годиннику капітана. Його улюблене заняття - бігати по колу, ніби він намагається зловити власний хвіст (якби він у нього був). Легенда свідчить, що він з'явився після того, як древній морський чарівник випадково оживив зуб гігантської акули.\nОсобливості:\n1.Постійний рух: Tooth невтомно бігає по колу, ніби намагається втекти від зубного болю.\n2.Життєдайні укуси: При зіткненні з піратом, Tooth "кусає" його, забираючи одне життя. Пірати жартують, що це помста за всі ті зуби, які вони втратили в бійках.\n3.Боязкий відступ: Якщо пірат атакує Tooth, той миттєво змінює напрямок руху, ніби згадавши про важливу зустріч на іншому кінці острова.\nЦікаві факти:\n1.Моряки вірять, що Tooth - це втілення духу всіх загублених зубів піратів.\n2.Деякі капітани використовують зображення Tooth на своїх прапорах, щоб відлякувати забобонних ворогів.\n3.Існує повір'я, що якщо пірату вдасться спіймати Tooth, то він ніколи більше не матиме проблем із зубами.""",
            "Shell": """Це підступний страж піратських скарбів, відомий своєю неперевершеною точністю та терпінням. Цей хитрий молюск обрав тактику "стій та стріляй", перетворивши свою мушлю на неприступну фортецю.\nОсобливості:\n1.Нерухомий вартовий: Shell ніколи не покидає свого посту. Він вірить, що справжній воїн не бігає за здобиччю, а чекає, коли вона сама прийде до нього.\n2.Прицільна стрільба: Кожні три секунди Shell випускає перлину з хірургічною точністю. Він пишається тим, що жодна перлина не витрачена даремно.\n3.Зона ураження: Якщо ви потрапили в поле зору Shell, вважайте, що ви вже на мушці. Його очі-перископи не пропустять жодного руху.\n4.Перлинний град: Перлини Shell - це не просто прикраси. Кожна з них може відправити пірата "годувати риб".\n5.Відбивання атак: Shell грає в теніс? Ні, але якщо ви відіб'єте його перлину, вона полетить в іншому напрямку. Може, пощастить, і вона влучить у його товариша!\n6.Ахіллесова п'ята: Єдиний спосіб здолати цього молюска - це близький бій. Тільки гострий меч може пробити його захист.\nЦікаві факти\n1.Кажуть, що Shell колись був звичайною устрицею, але після того, як проковтнув магічну перлину, він виріс до неймовірних розмірів і отримав свої здібності.\n2.Пірати жартують, що якщо зібрати всі перлини, якими стріляв Shell, можна було б купити цілий флот кораблів.\n3.Деякі сміливці намагалися використовувати Shell як гарматну установку, прив'язавши його до корабля. Результат експерименту досі невідомий, як і доля експериментаторів."""
        }
        self.square_icons = {
            "Andriiko": '',
            "Flovnes": join('..', 'Python Game Tutorial', 'graphics', 'options', 'flovnes_square'),
            "Watashiva Kramar": join('..', 'Python Game Tutorial', 'graphics', 'options', 'kramar_square'),
            "Vasilko": join('..', 'Python Game Tutorial', 'graphics', 'options', 'vasilko_square'),
            "Levchenko": join('..', 'Python Game Tutorial', 'graphics', 'options', 'levchenko_square'),
        }

        self.rect_icons = {
            "Andriiko": '',
            "Flovnes": join('..', 'Python Game Tutorial', 'graphics', 'options', 'flovnes_square'),
            "Watashiva Kramar": join('..', 'Python Game Tutorial', 'graphics', 'options', 'kramar_square'),
            "Vasilko": join('..', 'Python Game Tutorial', 'graphics', 'options', 'vasilko_rect'),
            "Levchenko": '',
        }
        self.players = [
            CurrentPlayer("Vasilko", self.square_icons["Vasilko"], self.rect_icons["Vasilko"], self.informations["Vasilko"]),
            CurrentPlayer("Andriiko", "path/to/square1.png", "path/to/vertical1.png", self.informations["Andriiko"]),
            CurrentPlayer("Flovnes", self.square_icons["Flovnes"], "path/to/vertical2.png", self.informations["Flovnes"]),
            CurrentPlayer("Watashiva Kramar", self.square_icons["Watashiva Kramar"], "path/to/vertical3.png", self.informations["Watashiva Kramar"]),
            CurrentPlayer("Levchenko", self.square_icons["Levchenko"], self.rect_icons["Levchenko"], self.informations["Levchenko"])
        ]

        # Create some enemy instances
        self.enemies = [
            Enemy("Tooth", join('..', 'Python Game Tutorial', 'graphics', 'enemies', 'tooth', 'run', '2.png'), join('..', 'Python Game Tutorial', 'graphics', 'enemies', 'tooth', 'run'), self.informations["Tooth"]),
            Enemy("Shell", join('..', 'Python Game Tutorial', 'graphics', 'enemies', 'shell', 'fire', '0.png'), join('..', 'Python Game Tutorial', 'graphics', 'enemies', 'shell', 'fire'), self.informations["Shell"]),
        ]


        # Add tabs
        self.settingsTab = SettingsTab(self.players)
        self.audioTab = AudioTab()
        self.movementGuideTab = MovementGuideTab()
        self.infoTab = InfoTab()
        self.creditsTab = CreditsTab()
        self.enemiesTab = EnemiesTab(self.enemies)

        self.tabWidget.addTab(self.settingsTab, "Settings")
        self.tabWidget.addTab(self.audioTab, "Audio")
        self.tabWidget.addTab(self.movementGuideTab, "Movement Guide")
        self.tabWidget.addTab(self.infoTab, "Info")
        self.tabWidget.addTab(self.creditsTab, "Credits")
        self.tabWidget.addTab(self.enemiesTab, "Enemies info")

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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Game Options"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), _translate("MainWindow", "Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.audioTab), _translate("MainWindow", "Audio"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.movementGuideTab), _translate("MainWindow", "Movement Guide"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.infoTab), _translate("MainWindow", "Info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.creditsTab), _translate("MainWindow", "Credits"))

