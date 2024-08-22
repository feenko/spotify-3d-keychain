import os
import platform
from typing import Dict, Tuple, Union

from PySide6.QtGui import QFont, QFontDatabase


class FontLoader:
    @staticmethod
    def load_font(font_path: str) -> Union[QFont, None]:
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id == -1:
            print(f"Failed to load font: {font_path}")
            return QFont()
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            print(f"Loaded font: {font_family}")
            return QFont(font_family)

    @staticmethod
    def load_fonts(fonts: dict[str, str]) -> Dict[str, QFont]:
        loaded_fonts = {}

        for font_name, font_path in fonts.items():
            font = FontLoader.load_font(font_path)
            loaded_fonts[font_name] = font

        return loaded_fonts


class Folder:
    @staticmethod
    def make_folder():
        os.makedirs(Folder.get_folder_path(), exist_ok=True)

    @staticmethod
    def get_folder_path() -> str:
        if (
            platform.system() == "Windows"
            or platform.system() == "Darwin"
            or platform.system() == "Linux"
        ):
            return os.path.join(
                os.path.expanduser("~"), "Documents", "Spotify Keychains"
            )
        else:
            raise NotImplementedError("Unsupported platform")

    @staticmethod
    def get_next_file_path() -> str:
        folder_path = Folder.get_folder_path()
        files = [file for file in os.listdir(folder_path) if file.endswith(".stl")]
        return os.path.join(folder_path, f"keychain_{len(files) + 1}.stl")


class SpotifyLinkParser:
    @staticmethod
    def parse_link(share_link: str) -> Union[Tuple[str, str], None]:
        """
        Extracts the type and URI from a Spotify share link.

        Parameters
        ----------
        share_link : str
            A Spotify share link that may contain track, album, artist, or playlist identifiers.

        Returns
        -------
        Union[Tuple[str, str], None]
            A tuple containing the type and URI of the Spotify resource if found, otherwise None.

        Example
        --------
        >>> SpotifyLinkParser.parse_link("https://open.spotify.com/track/5Q6f5I2abTY6yD9QhvYwwc")
        ('track', '5Q6f5I2abTY6yD9QhvYwwc')
        """
        base_link = share_link.split("?")[0]
        parts = base_link.split("/")

        valid_types = {"track", "album", "artist", "playlist"}

        for i in range(1, len(parts) - 1):
            if parts[i] in valid_types:
                return (parts[i], parts[i + 1])

        return None
