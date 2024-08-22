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


class SpotifyURL:
    @staticmethod
    def get_link_data(share_link: str) -> Union[Tuple[str, str], None]:
        """
        Extracts the type and URI from a Spotify share link.

        Args:
            share_link (str): The Spotify share link.

        Returns:
            Union[Tuple[str, str], None]: The type and URI if found, None otherwise
        """
        link = share_link.split("?")[0]
        parts = share_link.split("/")

        for i, part in enumerate(parts):
            if part in ["track", "album", "artist", "playlist"]:
                if i + 1 < len(parts):
                    return (part, parts[i + 1])

        return None
