import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt
from settings import *
from game_play import Game
from options import Ui_MainWindow

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Menu')
        self.setFixedSize(1280, 720)  # Set window size equivalent to your Pygame window

        # Set background using stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('../Python Game Tutorial/graphics/menu/main_menu/Background');
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        # Create central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title = QLabel('Pirates Adventure', self)
        self.title.setFont(QFont('../Python Game Tutorial/graphics/menu/main_menu/font.ttf', 70))
        self.title.setStyleSheet('color: #b68f40;')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        # Play Button
        self.play_button = QPushButton(self)
        self.play_button.setIcon(QIcon(QPixmap('../Python Game Tutorial/graphics/menu/main_menu/Play Rect')))
        self.play_button.setText('PLAY')
        self.play_button.setFont(QFont('../Python Game Tutorial/graphics/menu/main_menu/font.ttf', 75))
        self.play_button.setStyleSheet('color: #d7fcd4; background-color: transparent;')
        self.play_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.play_button)

        # Options Button
        self.options_button = QPushButton(self)
        self.options_button.setIcon(QIcon(QPixmap('../Python Game Tutorial/graphics/menu/main_menu/Options Rect')))
        self.options_button.setText('OPTIONS')
        self.options_button.setFont(QFont('../Python Game Tutorial/graphics/menu/main_menu/font.ttf', 75))
        self.options_button.setStyleSheet('color: #d7fcd4; background-color: transparent;')
        self.options_button.clicked.connect(self.open_options)
        self.layout.addWidget(self.options_button)

        # Quit Button
        self.quit_button = QPushButton(self)
        self.quit_button.setIcon(QIcon(QPixmap('../Python Game Tutorial/graphics/menu/main_menu/Quit Rect')))
        self.quit_button.setText('QUIT')
        self.quit_button.setFont(QFont('../Python Game Tutorial/graphics/menu/main_menu/font.ttf', 75))
        self.quit_button.setStyleSheet('color: #d7fcd4; background-color: transparent;')
        self.quit_button.clicked.connect(self.close_application)
        self.layout.addWidget(self.quit_button)

    def start_game(self):
        # Here you would call your game logic
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
    app.exec()
