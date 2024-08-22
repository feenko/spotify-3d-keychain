from copy import copy

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QMainWindow, QPushButton

from helpers.actions import generate_model, show_in_folder
from helpers.utils import FontLoader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize window
        self.setFixedSize(480, 329)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.setWindowTitle("Spotify Keychain — 3D Model Generator")

        # Load fonts
        font_light, font_regular, font_medium = FontLoader.load_fonts(
            {
                "Poppins-Light": "assets/fonts/Poppins-Light.ttf",
                "Poppins-Regular": "assets/fonts/Poppins-Regular.ttf",
                "Poppins-Medium": "assets/fonts/Poppins-Medium.ttf",
            }
        ).values()

        # Title
        self.title = QLabel("Spotify Keychain Generator", self)

        font = copy(font_medium)
        font.setPointSize(20)

        self.title.setFont(font)
        self.title.setGeometry(0, 0, 480, 100)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.show()

        # Horizontal rule
        self.hr = QLabel(self)
        self.hr.setGeometry(0, 100, 480, 1)
        self.hr.setStyleSheet("background-color: #2e2e2e;")
        self.hr.show()

        # Spotify URL Field (Label)
        self.spotify_url_label = QLabel("Spotify URL", self)

        font = copy(font_regular)
        font.setPointSize(11)

        self.spotify_url_label.setFont(font)
        self.spotify_url_label.setGeometry(20, 110, 440, 30)
        self.spotify_url_label.setStyleSheet("color: #ffffff;")
        self.spotify_url_label.show()

        # Spotify URL Field (Input)
        self.spotify_url_input = QLineEdit(self)
        self.spotify_url_input.setGeometry(20, 140, 440, 35)
        self.spotify_url_input.setStyleSheet(
            """
            color: #ffffff;
            background-color: #2e2e2e;
            border-radius: 4px;
            margin-top: 5px;
            font-size: 16px;
            padding: 2px;
            """
        )
        self.spotify_url_input.show()

        # Generate Button
        self.generate_button = QPushButton("Generate Model", self)
        self.generate_button.clicked.connect(
            lambda: generate_model(self.spotify_url_input.text(), self)
        )

        font = copy(font_medium)
        font.setPointSize(12)

        self.generate_button.setFont(font)
        self.generate_button.setGeometry(20, 190, 220 - 4, 50)
        self.generate_button.setStyleSheet(
            """
            QPushButton {
                color: #ffffff;
                background-color: #1db954;
                border-radius: 4px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #169c44;
            }
            QPushButton:pressed {
                background-color: #128438;
            }
            """
        )
        self.generate_button.show()

        # Show in Folder Button
        self.show_in_folder_button = QPushButton("Show in Folder", self)
        self.show_in_folder_button.clicked.connect(show_in_folder)

        font = copy(font_medium)
        font.setPointSize(12)

        self.show_in_folder_button.setFont(font)
        self.show_in_folder_button.setGeometry(240 + 4, 190, 220 - 4, 50)
        self.show_in_folder_button.setStyleSheet(
            """
            QPushButton {
                color: #ffffff;
                background-color: #2e2e2e;
                border-radius: 4px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #292929;
            }
            QPushButton:pressed {
                background-color: #232323;
            }
            """
        )
        self.show_in_folder_button.show()

        # Horizontal rule
        self.hr = QLabel(self)
        self.hr.setGeometry(0, 260, 480, 1)
        self.hr.setStyleSheet("background-color: #2e2e2e;")
        self.hr.show()

        # Status Label
        self.status_label = QLabel("Status: Ready", self)

        font = copy(font_regular)
        font.setPointSize(10)

        self.status_label.setFont(font)
        self.status_label.setGeometry(20, 270, 440, 30)
        self.status_label.setStyleSheet("color: #999999;")
        self.status_label.show()

        # Github Link
        self.view_on_github = QLabel(
            'View source on <a href="https://github.com/feenko/spotify-3d-keychain" style="color: #1db954; text-decoration: none;">GitHub</a>',
            self,
        )

        self.view_on_github.setFont(font)
        self.view_on_github.setOpenExternalLinks(True)
        self.view_on_github.setGeometry(20, 295, 440, 20)
        self.view_on_github.setStyleSheet("color: #999999;")
        self.view_on_github.show()

        self.show()

    def set_status(self, status: str):
        self.status_label.setText(f"Status: {status}")
        self.status_label.show()
