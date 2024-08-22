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
    Opens the result folder in the file explorer.
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

    Args:
        spotify_url (str): The Spotify URL input.
        window (Any): The window object to set the status.

    Returns:
        None
    """
    spotify_url_data = SpotifyLinkParser.parse_link(spotify_url)

    if spotify_url_data is None:
        window.set_status("Invalid Spotify URL")
        return None

    spotify_code_url = (
        "https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2F000000%2Fwhite%2F640%2Fspotify%3A"
        + spotify_url_data[0]
        + "%3A"
        + spotify_url_data[1]
    )

    response = requests.get(spotify_code_url)

    if not response.ok or not response.content:
        window.set_status("Failed to generate model (1)")
        return None

    FolderUtils.create_folder()

    img = Image.open(io.BytesIO(response.content)).crop((160, 0, 640 - 31, 160))
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

    print()
    print(f"There are {len(bar_heights)} bars of heights")

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

    return None
