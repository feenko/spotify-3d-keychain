import io
import os
import platform
import subprocess
from typing import Any

import cadquery as cq
import requests
from PIL import Image

from helpers.utils import FolderUtils, SpotifyLinkParser


def show_in_folder() -> None:
    """
    Opens the result folder in the file explorer. (Windows, macOS, Linux)

    Raises
    ------
    NotImplementedError
        If the platform is not supported
    """
    FolderUtils.create_folder()
    folder_path = FolderUtils.get_folder_path()

    if platform.system() == "Windows":
        os.startfile(folder_path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", folder_path])
    elif platform.system() == "Linux":
        subprocess.Popen(["xdg-open", folder_path])
    else:
        raise NotImplementedError("Unsupported platform")


def generate_model(spotify_url: str, window: Any) -> None:
    """
    Generates a model based on the Spotify URL input.

    Parameters
    ----------
    spotify_url : str
        The Spotify URL input
    window : Any
        The main window
    """
    spotify_url_data = SpotifyLinkParser.parse_link(spotify_url)

    if spotify_url_data is None:
        window.set_status("Invalid Spotify URL")
        return

    spotify_code_url = (
        "https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2F000000%2Fwhite%2F640%2Fspotify%3A"
        + spotify_url_data[0]
        + "%3A"
        + spotify_url_data[1]
    )

    try:
        response = requests.get(spotify_code_url)
        response.raise_for_status()
    except requests.RequestException:
        window.set_status("Failed to generate model. This might be issue with the SpotifyCodes API.")
        return

    FolderUtils.create_folder()

    try:
        img = Image.open(io.BytesIO(response.content)).crop((160, 0, 609, 160))
    except (IOError, ValueError):
        window.set_status("Failed to process image. Please try again.")
        return

    width, height = img.size
    img = img.load()

    bar_heights = []
    max_bar_height = 0

    for x in range(width):
        at_bar = False
        curr_height = 0

        for y in range(height):
            if img[x, y][0] > 20 or img[x, y][1] > 20 or img[x, y][2] > 20:
                at_bar = True
                curr_height += 1

        if at_bar and curr_height > max_bar_height:
            max_bar_height = curr_height / 20
        elif not at_bar and max_bar_height > 0:
            bar_heights.append(max_bar_height)
            max_bar_height = 0

    print(f"\nThere are {len(bar_heights)} bars of heights")
    for i, bar in enumerate(bar_heights):
        print(f"Bar {i + 1}: {bar}")

    model = cq.importers.importStep("assets/models/spotify_keychain.step")

    curr_bar = 0
    for bar in bar_heights:
        model = (
            model.pushPoints([(15.5 + curr_bar * 1.88, 7.5)])
            .sketch()
            .slot(9 / 5 * bar, 1, 90)
            .finalize()
            .extrude(4)
        )
        curr_bar += 1

    cq.exporters.export(model, FolderUtils.get_next_file_path())
    window.set_status("Model generated successfully, check the folder!")
