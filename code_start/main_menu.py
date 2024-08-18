import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize
from settings import *
from game_play import Game
from options import Ui_MainWindow

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pirates Adventure')
        self.setFixedSize(1280, 720)

        # Set background using stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('../Python Game Tutorial/graphics/menu/main_menu/Background');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
            QPushButton {
                color: #d7fcd4;
                background-color: rgba(0, 0, 0, 100);
                border: 2px solid #b68f40;
                border-radius: 15px;
                padding: 10px;
                font-size: 30px;
            }
            QPushButton:hover {
                background-color: rgba(182, 143, 64, 100);
            }
        """)

        # Create central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(40)

        # Add spacer to push title up
        self.main_layout.addSpacerItem(QSpacerItem(-100, -100, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))

        # Title
        self.title = QLabel('Pirates Adventure', self)
        self.title.setFont(QFont('../Python Game Tutorial/graphics/menu/main_menu/font.ttf', 70))
        self.title.setStyleSheet('color: #b68f40; background-color: rgba(0, 0, 0, 100); border-radius: 50px; padding: 3px;')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.title)

        # Create buttons layout
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create buttons
        buttons = [
            ('PLAY', self.start_game),
            ('OPTIONS', self.open_options),
            ('QUIT', self.close_application)
        ]

        for text, callback in buttons:
            button = QPushButton(text, self)
            button.setFont(QFont('../Python Game Tutorial/graphics/menu/main_menu/font.ttf', 30))
            button.clicked.connect(callback)
            button.setFixedSize(300, 80)
            self.buttons_layout.addWidget(button)

        # Add buttons layout to main layout
        self.main_layout.addLayout(self.buttons_layout)

    def start_game(self):
        print('Game started')
        self.close()
        game = Game()
        game.run()

    def open_options(self):
        print('Options opened')
        self.options_window = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(self.options_window, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.options_window.show()

    def close_application(self):
        print('Application closed')
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())